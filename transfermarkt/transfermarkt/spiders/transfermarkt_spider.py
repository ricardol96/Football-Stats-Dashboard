import scrapy
from scrapy.utils.response import open_in_browser
from transfermarkt import items
from datetime import datetime

class TransfermarktSpiderSpider(scrapy.Spider):
    name = 'transfermarkt_spider'
    allowed_domains = ['www.transfermarkt.com']

    def start_requests(self):
        
        country_dict = {
            'England': 'https://www.transfermarkt.com/premier-league/marktwerte/wettbewerb/GB1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Germany': 'https://www.transfermarkt.com/1-bundesliga/marktwerte/wettbewerb/L1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Spain': 'https://www.transfermarkt.com/laliga/marktwerte/wettbewerb/ES1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Italy': 'https://www.transfermarkt.com/serie-a/marktwerte/wettbewerb/IT1/pos//detailpos/0/altersklasse/alle/plus/1',
            'France': 'https://www.transfermarkt.com/ligue-1/marktwerte/wettbewerb/FR1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Netherlands': 'https://www.transfermarkt.com/eredivisie/marktwerte/wettbewerb/NL1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Portugal': 'https://www.transfermarkt.com/liga-nos/marktwerte/wettbewerb/PO1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Turkey': 'https://www.transfermarkt.com/super-lig/marktwerte/wettbewerb/TR1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Russia': 'https://www.transfermarkt.com/premier-liga/marktwerte/wettbewerb/RU1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Belgium': 'https://www.transfermarkt.com/jupiler-pro-league/marktwerte/wettbewerb/BE1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Austria': 'https://www.transfermarkt.com/bundesliga/marktwerte/wettbewerb/A1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Switzerland': 'https://www.transfermarkt.com/super-league/marktwerte/wettbewerb/C1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Greece': 'https://www.transfermarkt.com/super-league-1/marktwerte/wettbewerb/GR1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Denmark': 'https://www.transfermarkt.com/superligaen/marktwerte/wettbewerb/DK1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Croatia': 'https://www.transfermarkt.com/supersport-hnl/marktwerte/wettbewerb/KR1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Scotland': 'https://www.transfermarkt.com/premiership/marktwerte/wettbewerb/SC1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Czech Republic': 'https://www.transfermarkt.com/fortuna-liga/marktwerte/wettbewerb/TS1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Norway': 'https://www.transfermarkt.com/eliteserien/marktwerte/wettbewerb/NO1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Sweden': 'https://www.transfermarkt.com/allsvenskan/marktwerte/wettbewerb/SE1/pos//detailpos/0/altersklasse/alle/plus/1',
            'Serbia': 'https://www.transfermarkt.com/super-liga-srbije/marktwerte/wettbewerb/SER1/pos//detailpos/0/altersklasse/alle/plus/1',
        }

        for country in country_dict:
            yield scrapy.Request(url=country_dict[country], 
                                callback=self.parse,
                                headers = {
                                'Authority': 'www.transfermarkt.com',
                                'Path':country_dict[country].split('www.transfermarkt.com')[-1],
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'Cache-Control': 'max-age=0',
                                'Sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                                'Sec-ch-ua-mobile': '?0',
                                'Sec-ch-ua-platform': '"Windows"',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
                                    },
                                meta={'dont_redirect': True,
                                      'league_country': country}
                                )
        
    
    def parse(self, response):
        item = items.TransfermarktItem()
        if response.status not in [200]:
            item['response_code'] = response.status
            item['url'] = response.url
            item['league_country'] = response.meta['league_country']
            item['updated_on'] = datetime.now().strftime('%Y/%m/%d')
            yield item
        else:
            item['league'] = response.xpath('//meta[@name="keywords"]/@content').get().split(',')[0]
            item['url'] = response.url
            item['response_code'] = response.status
            item['league_country'] = response.meta['league_country']
            item['updated_on'] = datetime.now().strftime('%Y/%m/%d')

            def convert_to_integer(value_str):
                value_str = value_str.replace('€', '').replace('m', '').strip()
                value_float = float(value_str)
                return int(value_float * 1000000)
            
            def convert_date_format(date_str):
                date_obj = datetime.strptime(date_str, '%b %d, %Y')
                formatted_date = date_obj.strftime('%Y/%m/%d')
                return formatted_date
            
            for player in response.xpath('//table[@class="items"]/tbody/tr'):
                item['name'] = player.xpath('./td[2]//a/@title').get()
                item['position'] = player.xpath('./td[2]/table/tr[2]/td/text()').get()
                item['nationality'] = player.xpath('./td[3]/img/@title').get()
                item['age'] = player.xpath('./td[4]/text()').get()
                item['club'] = player.xpath('./td[5]/a/@title').get()
                item['highest_market_value'] = convert_to_integer(player.xpath('./td[6]//text()').get())
                item['value_updated'] = convert_date_format(player.xpath('./td[6]/span/@title').get())
                item['market_value'] = convert_to_integer(player.xpath('./td[8]/a/text()').get())
                item['player_page'] = response.urljoin(player.xpath('./td[2]//a/@href').get())
                yield item
                