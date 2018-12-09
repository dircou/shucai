# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3,os
from scrapy import signals
from pydispatch import dispatcher
# from scrapy.xlib.pydispatch import dispatcher

class ShucaiPipeline(object):

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.get_path,signals.engine_started)
        dispatcher.connect(self.get_close,signals.engine_stopped)

    def process_item(self, item, spider):
        self.conn.execute('insert into shucai (id, name, lowest, average, highest, unit, date) values (NULL,?,?,?,?,?,?)',
                          (item['name'], item['lowest'], item['average'], item['highest'], item['unit'], item['date']))
        self.conn.commit()
        return item

    def get_path(self):
        df_file = 'ShuCai.db'
        if os.path.isfile(df_file):
            self.conn = sqlite3.connect(df_file)
        else:
            self.conn = sqlite3.connect(df_file)
            self.conn.execute('create table shucai ('
                              'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                              'name CHAR(10),'
                              'lowest REAL,'
                              'average REAL,'
                              'highest REAL,'
                              'unit CHAR(10),'
                              'date DATETIME)')
            self.conn.commit()

    def get_close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None