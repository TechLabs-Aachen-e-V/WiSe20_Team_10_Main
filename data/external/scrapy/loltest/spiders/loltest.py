# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import Game
from ..constants import XPATHS_LADDER, XPATHS_GAME


class Loltest(scrapy.Spider):
    name = 'loltest'
    pages = ['1','2','3','4','5','6','7','8','9','10']
    urls=[]
    allowed_domains = ['op.gg']
    servers = ['na','euw','jp','eune','oce','brazil','www']
    for server in servers:
        for i in pages:
            urls.append('http://'+server+'.op.gg/ranking/ladder/page='+i)
    start_urls = urls

    def _parse_champions(self, selector):
        for champion in selector:
            yield champion.xpath(XPATHS_GAME['_champion_name']).extract_first()

    def parse(self, response):
        summoners = response.xpath(XPATHS_LADDER['_summoners']).extract()
        for summoner in summoners:
            yield Request(url="http:"+summoner, callback=self.parse_games)

    def parse_games(self, response):
        matches = response.xpath(XPATHS_GAME['_matches'])
        for match in matches:
            summoners_t1 = match.xpath(XPATHS_GAME['_summoners_team_1'])
            summoners_t2 = match.xpath(XPATHS_GAME['_summoners_team_2'])
            match_type = match.xpath(XPATHS_GAME['_match_type']
                                     ).extract_first().strip()
            result = response.xpath(XPATHS_GAME['result']
                                    ).extract_first().strip()
            if match_type != 'Ranked Solo' or result == 'Remake':
                continue

            selector_t1 = match.xpath(XPATHS_GAME['_champions_team_1'])
            selector_t2 = match.xpath(XPATHS_GAME['_champions_team_2'])
            team_1 = list(self._parse_champions(selector_t1))
            team_2 = list(self._parse_champions(selector_t2))

            item = Game()
            result = match.xpath(
                XPATHS_GAME['result']).extract_first().strip()
            player = response.xpath(XPATHS_GAME['player']).extract_first()
            players_t1 = [summoner.xpath(
                          './/text()'
                          ).extract()[1] for summoner in summoners_t1]
            if player in players_t1:
                if result == 'Victory':
                    item['winner'] = 'Team 1'
                else:
                    item['winner'] = 'Team 2'
            else:
                if result == 'Victory':
                    item['winner'] = 'Team 2'
                else:
                    item['winner'] = 'Team 1'
            item['server'] = response.url.split('/')[2].split('.')[0]
            item['team_1'] = team_1
            item['team_2'] = team_2
            item['timestamp'] = match.xpath(XPATHS_GAME['timestamp']
                                            ).extract_first()
            item['duration'] = match.xpath(XPATHS_GAME['_duration']).get()
            item['summoner_name'] = player

            yield item
