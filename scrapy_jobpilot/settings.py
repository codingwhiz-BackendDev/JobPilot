BOT_NAME = "scrapy_jobpilot"

SPIDER_MODULES = ["scrapy_jobpilot.spiders"]
NEWSPIDER_MODULE = "scrapy_jobpilot.spiders"

# Be respectful by default.
ROBOTSTXT_OBEY = True

USER_AGENT = "Mozilla/5.0 (compatible; JobPilotBot/1.0)"

DOWNLOAD_DELAY = 1
AUTOTHROTTLE_ENABLED = True

LOG_LEVEL = "INFO"

ITEM_PIPELINES = {
    "scrapy_jobpilot.pipelines.django_pipeline.DjangoPipeline": 300,
}

