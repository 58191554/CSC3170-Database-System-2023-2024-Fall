# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class CsRanking2DbPipeline:

    def __init__(self):

        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'debian-sys-maint',
            password = 'R5jWqafHA3EVBULZ',
            database = 'cs_rank_db'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS cs_rank(
            name text, 
            rank_number int,
            city text,
            state text, 
            PRIMARY KEY (name(255))  -- Specify a key length (e.g., 255 characters)
        )
        """)

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(""" insert into cs_rank (name, rank_number, city, state) values (%s,%s,%s,%s)""", (
            item["name"],
            str(item["rank_number"]),
            item["city"], 
            item["state"]
        ))

        ## Execute insert of data into database
        self.conn.commit()

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()