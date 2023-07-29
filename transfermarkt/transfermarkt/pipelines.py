import mysql.connector

class TransfermarktPipeline:
    
    def __init__(self, db_settings):
        self.db_settings = db_settings

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict('MYSQL_SETTINGS')
        return cls(db_settings)

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(**self.db_settings)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""
                INSERT INTO players_value (
                    name, position, age, nationality, club,
                    market_value, highest_market_value, value_updated,
                    player_page, league, league_country, response_code, url, updated_on
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item['name'],
                item['position'],
                item['age'],
                item['nationality'],
                item['club'],
                item['market_value'],
                item['highest_market_value'],
                item['value_updated'],
                item['player_page'],
                item['league'],
                item['league_country'],
                item['response_code'],
                item['url'],
                item['updated_on']
            ))
            self.conn.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
        return item
