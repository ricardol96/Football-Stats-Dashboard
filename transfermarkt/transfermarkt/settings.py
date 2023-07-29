import os
from datetime import datetime

BOT_NAME = 'transfermarkt'

SPIDER_MODULES = ['transfermarkt.spiders']
NEWSPIDER_MODULE = 'transfermarkt.spiders'
ROBOTSTXT_OBEY = False
LOG_LEVEL = 'INFO'
date = datetime.now().strftime('%d/%m/%Y')
LOG_FILE = f'transfermarkt_{date}.log'

CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 0.01
COOKIES_ENABLED = False

SPIDER_MIDDLEWARES = {
   'transfermarkt.middlewares.TransfermarktSpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
   'transfermarkt.middlewares.TransfermarktDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
    'transfermarkt.pipelines.TransfermarktPipeline': 300,
}
MYSQL_SETTINGS = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': 'players'
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.01
AUTOTHROTTLE_MAX_DELAY = 0.05
USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'