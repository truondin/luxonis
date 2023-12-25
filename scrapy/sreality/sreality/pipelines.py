# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import sqlite3

import psycopg2
from itemadapter import ItemAdapter


class SrealityPipeline:

    def __init__(self):
        # self.con = sqlite3.connect('test.db')
        # self.cur = self.con.cursor()
        self.cur = None
        self.con = None
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.con = psycopg2.connect(
            dbname="sreality",
            user="postgres",
            password="password",
            host="postgres",
            port="5432"
        )
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        self.cur.execute("""CREATE TABLE IF NOT EXISTS 
                Properties(
                p_id uuid DEFAULT uuid_generate_v4(), 
                title TEXT,
                img_url TEXT,
                PRIMARY KEY (p_id))
        """)
        self.con.commit()

    def insert_item(self, item):
        try:
            self.cur.execute("""INSERT INTO Properties(title, img_url) VALUES (%s, %s)""",
                             (item['title'], item['img']))
        except BaseException as e:
            print(e)
        self.con.commit()

    def process_item(self, item, spider):
        self.insert_item(item)

        return item
