import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run Scrapy spider to scrape We Work Remotely jobs into the Django database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--term",
            default="django",
            help="Search term used on We Work Remotely (default: django).",
        )
        parser.add_argument(
            "--max-jobs",
            type=int,
            default=50,
            help="Maximum number of job detail pages to save (default: 50).",
        )

    def handle(self, *args, **options):
        # Ensure Django can be imported by Scrapy pipeline (which uses ORM).
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JobPilot.settings")

        term = options["term"]
        max_jobs = options["max_jobs"]

        # Tell Scrapy which settings module to use for this spider.
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "scrapy_jobpilot.settings")

        from scrapy.crawler import CrawlerProcess
        from scrapy.utils.project import get_project_settings

        scrapy_settings = get_project_settings()

        process = CrawlerProcess(scrapy_settings)
        process.crawl(
            "weworkremotely",
            term=term,
            max_jobs=max_jobs,
        )
        process.start()

        self.stdout.write(self.style.SUCCESS("Scrape finished."))

