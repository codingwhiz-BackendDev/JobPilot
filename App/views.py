import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Job
from django.utils import timezone
from datetime import timedelta


def index(request):
    jobs = Job.objects.all()[:10]
    context = {'jobs': jobs}
    return render(request, "index.html", context)


def jobs(request):
    jobs_list = []
    cached_jobs = None

    if request.method == "POST":
        query = request.POST.get("query", "").lower().strip()

        print("\n===== JOB SCRAPER STARTED =====")
        print("User searched for:", query)

        cached_jobs = Job.objects.filter(title__icontains=query).order_by('-created_at')

        CACHE_DURATION = timedelta(days=1)

        if cached_jobs.exists():
            latest_job = cached_jobs.first()

            if latest_job.created_at > timezone.now() - CACHE_DURATION:
                print("Using cached jobs")
                print("Cached jobs:", cached_jobs.count())

                jobs_list = list(
                    cached_jobs.values('title', 'company', 'location', 'link')
                )

                return render(request, "jobs.html", {
                    "jobs": jobs_list,
                    "cached_jobs": cached_jobs
                })
        else:
            print("No cached jobs found. Scraping sites...")

        search_words = query.split()

        try:

            # -------------------------
            # RemoteOK
            # -------------------------
            # print("\nFetching jobs from RemoteOK...")
            # response = requests.get(
            #     "https://remoteok.com/api",
            #     headers={"User-Agent": "Mozilla/5.0"},
            #     timeout=10
            # )
            # data = response.json()

            # print("RemoteOK jobs received:", len(data) - 1)

            # for job in data[1:]:
            #     title = (job.get("position") or "").lower()
            #     company = job.get("company") or "Unknown"
            #     location = (job.get("location") or "remote").lower()
            #     link = job.get("url")

            #     if search_words and not any(word in title for word in search_words):
            #         continue

            #     job_obj, created = Job.objects.get_or_create(
            #         link=link,
            #         defaults={
            #             "title": title.title(),
            #             "company": company,
            #             "location": location.title(),
            #         }
            #     )

            #     jobs_list.append({
            #         "title": job_obj.title,
            #         "company": job_obj.company,
            #         "location": job_obj.location,
            #         "link": job_obj.link
            #     })

            #     if created:
            #         print("RemoteOK NEW JOB:", job_obj)

            # -------------------------
            # Remotive
            # -------------------------
            print("\nFetching jobs from Remotive...")
            response = requests.get(
                "https://remotive.com/api/remote-jobs",
                timeout=10
            )
            data = response.json()

            print("Remotive jobs received:", len(data["jobs"]))

            for job in data["jobs"]:
                title = (job.get("title") or "").lower()
                company = job.get("company_name") or "Unknown"
                link = job.get("url")

                if search_words and not any(word in title for word in search_words):
                    continue

                job_obj, created = Job.objects.get_or_create(
                    link=link,
                    defaults={
                        "title": title.title(),
                        "company": company,
                        "location": "Remote",
                    }
                )

                jobs_list.append({
                    "title": job_obj.title,
                    "company": job_obj.company,
                    "location": job_obj.location,
                    "link": job_obj.link
                })

                if created:
                    print("Remotive NEW JOB:", job_obj)

            # -------------------------
            # Arbeitnow
            # -------------------------
            print("\nFetching jobs from Arbeitnow...")
            response = requests.get(
                "https://www.arbeitnow.com/api/job-board-api",
                timeout=10
            )
            data = response.json()

            print("Arbeitnow jobs received:", len(data["data"]))

            for job in data["data"]:
                title = (job.get("title") or "").lower()
                company = job.get("company_name") or "Unknown"
                location = (job.get("location") or "Remote")
                link = job.get("url")

                if search_words and not any(word in title for word in search_words):
                    continue

                job_obj, created = Job.objects.get_or_create(
                    link=link,
                    defaults={
                        "title": title.title(),
                        "company": company,
                        "location": location,
                    }
                )

                jobs_list.append({
                    "title": job_obj.title,
                    "company": job_obj.company,
                    "location": job_obj.location,
                    "link": job_obj.link
                })

                if created:
                    print("Arbeitnow NEW JOB:", job_obj)

            # -------------------------
            # Remote.co (with retry — up to 3 attempts)
            # -------------------------
            print("\nFetching jobs from Remote.co...")

            REMOTE_CO_HEADERS = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

            remote_co_query = query.replace(" ", "+")
            remote_co_url = f"https://remote.co/remote-jobs/search/?search_keywords={remote_co_query}"
            remote_co_response = None

            for attempt in range(1, 4):  # 3 attempts max
                try:
                    print(f"Remote.co attempt {attempt}...")
                    remote_co_response = requests.get(
                        remote_co_url,
                        headers=REMOTE_CO_HEADERS,
                        timeout=10,
                    )
                    if remote_co_response.status_code == 200:
                        print("Remote.co succeeded on attempt", attempt)
                        break
                    else:
                        print(f"Remote.co attempt {attempt} returned status {remote_co_response.status_code}")
                except requests.exceptions.Timeout:
                    print(f"Remote.co attempt {attempt} timed out.")
                except requests.exceptions.RequestException as e:
                    print(f"Remote.co attempt {attempt} error: {e}")
                    break  # non-recoverable error, stop retrying

            if remote_co_response and remote_co_response.status_code == 200:
                soup = BeautifulSoup(remote_co_response.text, "html.parser")

                cards = (
                    soup.select("li.job_listing")
                    or soup.select(".card.m-0")
                    or soup.select("[data-job-id]")
                )

                print("Remote.co jobs found:", len(cards))

                for card in cards[:10]:
                    title_tag = (
                        card.select_one(".position")
                        or card.select_one("h2")
                        or card.select_one("h3")
                        or card.select_one("a")
                    )
                    company_tag = (
                        card.select_one(".company")
                        or card.select_one(".company_name")
                    )
                    link_tag = card.select_one("a[href]")

                    if not title_tag:
                        continue

                    title = title_tag.get_text(strip=True).lower()
                    company = company_tag.get_text(strip=True) if company_tag else "Unknown"
                    link = link_tag["href"] if link_tag else ""

                    if link and link.startswith("/"):
                        link = "https://remote.co" + link

                    if search_words and not any(word in title for word in search_words):
                        continue

                    if not link:
                        continue

                    job_obj, created = Job.objects.get_or_create(
                        link=link,
                        defaults={
                            "title": title.title(),
                            "company": company,
                            "location": "Remote",
                        }
                    )

                    jobs_list.append({
                        "title": job_obj.title,
                        "company": job_obj.company,
                        "location": job_obj.location,
                        "link": job_obj.link
                    })

                    if created:
                        print("Remote.co NEW JOB:", job_obj)
            else:
                print("Remote.co failed after all attempts, skipping.")

            # -------------------------
            # Adzuna
            # -------------------------
            print("\nFetching jobs from Adzuna...")

            ADZUNA_APP_ID = "0b6cb544"
            ADZUNA_APP_KEY = "8cc0d13f2d15e24bbf813268afaee354"

            adzuna_query = query.replace(" ", "%20")
            url = (
                f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
                f"?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
                f"&results_per_page=20&what={adzuna_query}"
            )

            response = requests.get(url, timeout=10)
            data = response.json()

            results = data.get("results", [])
            print("Adzuna jobs received:", len(results))

            for job in results:
                title = (job.get("title") or "").lower()
                company = (job.get("company") or {}).get("display_name") or "Unknown"
                location = (job.get("location") or {}).get("display_name") or "Unknown"
                link = job.get("redirect_url") or job.get("url") or ""

                if search_words and not any(word in title for word in search_words):
                    continue

                if not link:
                    continue

                job_obj, created = Job.objects.get_or_create(
                    link=link,
                    defaults={
                        "title": title.title(),
                        "company": company,
                        "location": location,
                    }
                )

                jobs_list.append({
                    "title": job_obj.title,
                    "company": job_obj.company,
                    "location": job_obj.location,
                    "link": job_obj.link
                })

                if created:
                    print("Adzuna NEW JOB:", job_obj)

            # -------------------------
            # We Work Remotely — via RSS feeds (bypasses Cloudflare 403)
            #
            # WWR blocks HTML scraping via Cloudflare, but their RSS feeds are
            # fully public and never blocked. We fetch all major category feeds
            # and filter results by the user's search query locally.
            # -------------------------
            print("\nFetching jobs from We Work Remotely (RSS)...")

            WWR_RSS_FEEDS = [
                "https://weworkremotely.com/categories/remote-programming-jobs.rss",
                "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
                "https://weworkremotely.com/categories/remote-design-jobs.rss",
                "https://weworkremotely.com/categories/remote-marketing-jobs.rss",
                "https://weworkremotely.com/categories/remote-product-jobs.rss",
                "https://weworkremotely.com/categories/remote-customer-support-jobs.rss",
                "https://weworkremotely.com/categories/remote-sales-jobs.rss",
                "https://weworkremotely.com/categories/remote-writing-jobs.rss",
                "https://weworkremotely.com/categories/remote-business-exec-management-jobs.rss",
                "https://weworkremotely.com/categories/remote-finance-legal-jobs.rss",
                "https://weworkremotely.com/categories/remote-human-resources-jobs.rss",
                "https://weworkremotely.com/categories/remote-data-science-jobs.rss",
            ]

            WWR_RSS_HEADERS = {
                "User-Agent": "Mozilla/5.0 (compatible; RSS reader)",
                "Accept": "application/rss+xml, application/xml, text/xml",
            }

            wwr_total = 0

            for feed_url in WWR_RSS_FEEDS:
                try:
                    rss_response = requests.get(
                        feed_url,
                        headers=WWR_RSS_HEADERS,
                        timeout=10,
                    )

                    if rss_response.status_code != 200:
                        print(f"WWR RSS feed returned {rss_response.status_code}: {feed_url}")
                        continue

                    root = ET.fromstring(rss_response.content)
                    channel = root.find("channel")

                    if channel is None:
                        continue

                    items = channel.findall("item")

                    for item in items:
                        # RSS <title> format: "CompanyName: Job Title"
                        raw_title = (item.findtext("title") or "").strip()
                        link = (item.findtext("link") or "").strip()
                        region = (item.findtext("region") or "Remote").strip()

                        # Split "Company: Title" format
                        if ": " in raw_title:
                            parts = raw_title.split(": ", 1)
                            company = parts[0].strip()
                            title = parts[1].strip().lower()
                        else:
                            company = "Unknown"
                            title = raw_title.lower()

                        if not link or not title:
                            continue

                        # Filter by search query
                        if search_words and not any(word in title for word in search_words):
                            continue

                        job_obj, created = Job.objects.get_or_create(
                            link=link,
                            defaults={
                                "title": title.title(),
                                "company": company,
                                "location": region if region else "Remote",
                            }
                        )

                        jobs_list.append({
                            "title": job_obj.title,
                            "company": job_obj.company,
                            "location": job_obj.location,
                            "link": job_obj.link
                        })

                        wwr_total += 1

                        if created:
                            print("We Work Remotely NEW JOB:", job_obj)

                except requests.exceptions.Timeout:
                    print(f"WWR RSS feed timed out: {feed_url}")
                except ET.ParseError as e:
                    print(f"WWR RSS parse error for {feed_url}: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"WWR RSS request error for {feed_url}: {e}")

            print(f"We Work Remotely jobs collected: {wwr_total}")

            print("\nTotal jobs collected:", len(jobs_list))
            print("===== SCRAPER FINISHED =====\n")

        except Exception as e:
            print("Error:", e)

    return render(request, "jobs.html", {
        "jobs": jobs_list,
        "cached_jobs": cached_jobs
    })
    
def saved_jobs(request):
    return render(request, "jobs.html")

def job_details(request):
    return render(request, "job_details.html")

def companies(request):
    return render(request, "companies.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")