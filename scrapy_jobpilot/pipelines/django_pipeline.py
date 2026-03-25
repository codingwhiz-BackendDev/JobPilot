import os


class DjangoPipeline:
    """
    Persist scraped items into your Django database.

    This pipeline boots Django when Scrapy starts so it can use the ORM.
    """

    def __init__(self):
        self._django_ready = False

    def open_spider(self, spider):
        if self._django_ready:
            return

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JobPilot.settings")

        import django  # noqa

        django.setup()
        self._django_ready = True

    def process_item(self, item, spider):
        from App.models import Company, Job

        company_name = (item.get("company_name") or "").strip()
        if not company_name:
            # Skip bad items (parsing failed).
            return item

        company, _ = Company.objects.get_or_create(
            name=company_name,
            defaults={
                "website_url": item.get("company_website_url") or None,
                "location": item.get("company_location") or "",
                "description": item.get("company_description") or "",
            },
        )

        # Keep job uniqueness stable using the job URL.
        job_url = item.get("job_url")
        if not job_url:
            return item

        Job.objects.update_or_create(
            job_url=job_url,
            defaults={
                "company": company,
                "title": item.get("title") or "",
                "location": item.get("location") or "",
                "job_type": item.get("job_type") or "",
                "salary": item.get("salary") or "",
                "salary_range": item.get("salary_range") or "",
                "tags": item.get("tags") or [],
                "posted_text": item.get("posted_text") or "",
                "description": item.get("description") or "",
                "apply_url": item.get("apply_url") or None,
                "scraped_term": item.get("scraped_term") or "",
            },
        )

        return item

