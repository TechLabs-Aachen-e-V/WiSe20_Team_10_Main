# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Game(scrapy.Item):
    timestamp = scrapy.Field()
    server = scrapy.Field()
    winner = scrapy.Field()
    team_1 = scrapy.Field()
    team_2 = scrapy.Field()
    summoner_name = scrapy.Field()
    duration = scrapy.Field()
