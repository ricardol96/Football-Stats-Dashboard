# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TransfermarktItem(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    age = scrapy.Field()
    nationality = scrapy.Field()
    club = scrapy.Field()
    market_value = scrapy.Field()
    highest_market_value = scrapy.Field()
    value_updated = scrapy.Field()
    player_page = scrapy.Field()
    league = scrapy.Field()
    league_country = scrapy.Field()
    response_code = scrapy.Field()
    updated_on = scrapy.Field()
    url = scrapy.Field()

