XPATHS_GAME = {
    'player': '//div[@class="Information"]/span//text()',
    '_matches': '//div[@class="GameItemWrap"]',
    'result': './/div[@class="GameResult"]/text()',
    '_match_type': './/div[@class="GameType"]/text()',
    '_champions_team_1': './/div[@class="Team"][1]//div[@class="ChampionImage"]',
    '_champions_team_2': './/div[@class="Team"][2]//div[@class="ChampionImage"]',
    '_summoners_team_1': './/div[@class="Team"][1]//div[@class="SummonerName"]',
    '_summoners_team_2': './/div[@class="Team"][2]//div[@class="SummonerName"]',
    '_champion_name': './/div/text()',
    'timestamp': './/div[@class="TimeStamp"]//span/text()',
    'profile_link': './/a/@href',
    '_duration':'.//div[@class="GameLength"]/text()'
}


XPATHS_LADDER = {
    '_summoners': '//a[not(contains(@class, "ranking-highest'
                  '__name"))]//@href[contains(.,"userName")]'
}
