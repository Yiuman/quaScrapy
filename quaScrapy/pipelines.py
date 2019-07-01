#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:yiuman
@time: 2019/07/01

"""

import pymysql
import json

from quaScrapy.items import AttractionsItem, EvaluationItem

class MysqlPipeline(object):
    def __init__(self, host, database, user, password, port, sql_file_name=None):
        # 去重id，保存前先从库中查询出来，数据插入时也将插入这个set中
        self.attractionsIds = set()
        self.evaluationIds = set()
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connect = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                       port=self.port)
        self.sql_file_name = sql_file_name
        if sql_file_name:
            fd = open(sql_file_name, 'r', encoding='utf-8')
            self.sqlFile = fd.read()
            fd.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
            sql_file_name=crawler.settings.get('INIT_TABLE_SQL_FILE'),
        )

    def open_spider(self, spider):
        with self.connect.cursor() as cursor:
            if self.sqlFile:
                for sql in self.sqlFile.split(";"):
                    try:
                        cursor.execute(sql)
                        print(sql)
                    except Exception as sqlMessage:
                        print(sqlMessage)

            cursor.execute('select id from `QUA_ATTRACTIONS`')
            for attractionsId in cursor.fetchall():
                self.attractionsIds.add(attractionsId[0])

            cursor.execute('select id from `QUA_EVALUATION`')
            for evaluationId in cursor.fetchall():
                self.evaluationIds.add(evaluationId[0])

    def close_spider(self, spider):
        self.connect.close()

    def process_item(self, item, spider):
        with self.connect.cursor() as cursor:
            data = dict(item)
            values = ', '.join(['%s'] * len(data))
            if isinstance(item, AttractionsItem):
                try:
                    if item['id'] not in self.attractionsIds:
                        cursor.execute(
                            'insert into QUA_ATTRACTIONS (ID,NAME,PRICE,SALES,HEAT,ADDRESS,SCORE) values (%s)' % (
                                values),
                            tuple(data.values()))
                        self.connect.commit()
                        self.attractionsIds.add(item['id'])
                except Exception as message:
                    print(message)
                    pass
            elif isinstance(item, EvaluationItem):
                try:
                    if item['id'] not in self.evaluationIds:
                        cursor.execute(
                            'insert into QUA_EVALUATION (ID,ITEM_ID,EVALUATION_TYPE,EVALUATION_TEXT,AUTHOR,CONTENT,CREATE_DATE,SCORE,IMGS,USER_NICKNAME) values (%s)' % (
                                values),
                            tuple(data.values()))
                        self.connect.commit()
                        self.evaluationIds.add(item['id'])
                except Exception as message:
                    print(message)
                    pass
        return item


class JsonWritePipeline(object):
    def __init__(self):
        self.qua_file = open("qua_file.json", "w")
        self.evaluation_file = open("evaluation_file.json", "w")

    def process_item(self, item, spider):
        if isinstance(item, AttractionsItem):
            try:
                text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
                self.qua_file.write(text)
            except Exception:
                pass
        elif isinstance(item, EvaluationItem):
            try:
                text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
                self.evaluation_file.write(text)
            except Exception:
                pass
        return item

    def close_spider(self):
        self.qua_file.close()
        self.evaluation_file.close()
