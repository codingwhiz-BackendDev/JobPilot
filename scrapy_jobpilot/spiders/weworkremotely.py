import re
from urllib.parse import urljoin

import scrapy


class WeWorkRemotelySpider(scrapy.Spider):
    """
    Scrape We Work Remotely job detail pages from the search results page.

    Note: this is a starter spider. WeWorkRemotely markup can change; you may need
    to tweak the XPath selectors / regex heuristics if fields come out empty.
    """

    name = "weworkremotely"
    allowed_domains = ["weworkremotely.com"]

    def __init__(self, term="django", max_jobs=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.term = term
        self.max_jobs = int(max_jobs)
        self.scraped_jobs = 0
        self.seen_job_urls = set()

        self.start_urls = [
            f"https://weworkremotely.com/remote-jobs/search?term={self.term}",
        ]

    def parse(self, response):
        # Collect job detail links from search results.
        # We filter out "search" links and keep only /remote-jobs/<slug> style URLs.
        hrefs = response.xpath('//a[contains(@href, "/remote-jobs/")]/@href').getall()
        for href in hrefs:
            if not href:
                continue
            if "search" in href:
                continue
            if "categories" in href:
                continue

            job_url = response.urljoin(href)
            if job_url in self.seen_job_urls:
                continue

            self.seen_job_urls.add(job_url)
            yield scrapy.Request(job_url, callback=self.parse_job, meta={"scraped_term": self.term})

            if self.scraped_jobs >= self.max_jobs:
                break

        # Follow pagination if it exists.
        next_href = (
            response.xpath('//a[@rel="next"]/@href').get()
            or response.xpath('//a[contains(., "Next")]/@href').get()
        )
        if next_href and self.scraped_jobs < self.max_jobs:
            yield response.follow(next_href, callback=self.parse)

    def parse_job(self, response):
        from scrapy.exceptions import CloseSpider

        if self.scraped_jobs >= self.max_jobs:
            raise CloseSpider("max_jobs_reached")

        scraped_term = response.meta.get("scraped_term", "")

        title = response.xpath("normalize-space(//h1)").get()
        title = title.strip() if title else ""

        company_name = response.xpath('(//a[contains(@href, "/company/")])[1]//text()').get()
        company_name = company_name.strip() if company_name else ""

        job_type = ""
        location = ""
        salary = ""
        salary_range = ""
        tags = []

        # Use full text from main/body and extract common labeled parts using regex.
        main_text = response.xpath("//main").xpath("string(.)").get()
        if not main_text:
            main_text = response.xpath("//body").xpath("string(.)").get()

        main_text = self._normalize_text(main_text or "")

        posted_text = self._extract_first(main_text, r"Posted\s+(.+?)(?:\n|$)")
        job_type = self._extract_first(
            main_text,
            r"Job type\s+(.+?)(?:\n|$)",
            default="",
        )
        location = self._extract_first(
            main_text,
            r"Region\s+(.+?)(?:\n|$)",
            default="",
        )

        location = self._normalize_location(location)
        job_type = self._normalize_job_type(job_type)

        # About / description: try to keep Role Overview-ish content only.
        description = self._extract_section(
            main_text,
            start_markers=[r"Role Overview", r"About the job", r"About this role"],
            end_markers=[r"Key Responsibilities", r"Required Skills", r"Required Skills & Experience", r"Nice to Have", r"Interested"],
        )
        if not description:
            # Fallback: store full main text (can be long, but better than blank).
            description = main_text[:5000]

        # Apply url can require an account; we still store it if present.
        apply_url = response.xpath(
            '//a[contains(@href, "/job-seekers/account/register")]/@href'
        ).get()

        item = {
            "job_url": response.url,
            "scraped_term": scraped_term,
            "title": title,
            "company_name": company_name,
            "company_website_url": None,
            "company_location": "",
            "company_description": "",
            "location": location,
            "job_type": job_type,
            "salary": salary,
            "salary_range": salary_range,
            "tags": tags,
            "posted_text": posted_text,
            "description": description,
            "apply_url": response.urljoin(apply_url) if apply_url else None,
        }

        self.scraped_jobs += 1
        yield item

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = re.sub(r"\s+\n", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @staticmethod
    def _extract_first(text: str, pattern: str, default: str = "") -> str:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        return m.group(1).strip() if m else default

    @staticmethod
    def _normalize_location(location: str) -> str:
        loc = (location or "").strip()
        if not loc:
            return ""

        if re.search(r"\bremote\b", loc, flags=re.I) or re.search(r"anywhere", loc, flags=re.I):
            return "Remote"
        if re.search(r"\busa\b", loc, flags=re.I) or re.search(r"united states", loc, flags=re.I):
            return "USA"
        if re.search(r"\buk\b", loc, flags=re.I) or re.search(r"united kingdom", loc, flags=re.I):
            return "UK"
        if re.search(r"\bcanada\b", loc, flags=re.I):
            return "Canada"
        return loc

    @staticmethod
    def _normalize_job_type(job_type: str) -> str:
        jt = (job_type or "").strip()
        if not jt:
            return ""

        # Match your frontend checkbox labels.
        if re.search(r"full", jt, flags=re.I):
            return "Full-time"
        if re.search(r"part", jt, flags=re.I):
            return "Part-time"
        if re.search(r"contract", jt, flags=re.I):
            return "Contract"
        return jt

    def _extract_section(self, text: str, start_markers: list[str], end_markers: list[str]) -> str:
        # Build a regex that finds one of the start markers and then captures until one of the end markers.
        start = "|".join(start_markers)
        end = "|".join(end_markers)
        pattern = rf"(?:{start})\s*(.+?)(?:{end})"
        m = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if not m:
            return ""
        section = m.group(1).strip()
        # Keep length reasonable for the DB.
        return section[:3000]

