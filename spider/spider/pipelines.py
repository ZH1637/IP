# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from multiprocessing import Queue

import pymysql

from config import MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_SET
from checkip.checkip import start_process
import time

from spider.spider.settings import MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB, MYSQL_CHAR


class IpPipeline(object):

    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(MONGO_HOST,MONGO_PORT)
        self.db = self.conn[MONGO_DB]
        self.myset = self.db[MONGO_SET]


class MysqlPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD,MYSQL_DB, charset=MYSQL_CHAR)
        self.cursor = self.db.cursor()
    def process_item(self,item,spider):








