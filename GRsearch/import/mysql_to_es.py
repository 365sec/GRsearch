#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import json
import urllib2
import traceback
import time
from datetime import date, datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, datetime.datetime):
        #     return int(mktime(obj.timetuple()))
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def mysql_to_es():
    tablename = raw_input("表：")
    conn = MySQLdb.connect(host='172.16.39.180', user='webscan', passwd='1qaz2wsx', db='liuren', port=3306, charset='utf8')
    cur = conn.cursor()
    piliang_nums = 50000
    startTime = time.time()
    es = Elasticsearch(hosts=["172.16.39.231","172.16.39.232","172.16.39.233","172.16.39.234"],timeout=5000)
    try:
        sql1 = "SELECT COLUMN_NAME FROM information_schema.COLUMNS where TABLE_SCHEMA = 'liuren' and TABLE_NAME = '" + tablename + "'"
        num_of_fields = cur.execute(sql1)
        data1 = cur.fetchall()
        a = 0
        listfield = []
        while a < num_of_fields:
            listfield.append(data1[a][0])
            a = a + 1
        print listfield
        sql2 = "SELECT COUNT(*) FROM " + tablename
        cur.execute(sql2)
        data2 = cur.fetchall()
        data_num = data2[0][0]
        print data_num
        j = 0
        while j < data_num:
            sql3 = "select * from " + tablename + " limit " + str(j) + "," + str(piliang_nums)
            cur.execute(sql3)
            data = cur.fetchall()
            actions = []
            for row in data:
                if row != None:
                    m = 0
                    source = {}
                    action = {}
                    while m < num_of_fields: 
                        source[listfield[m]] = row[m]
                        m = m + 1
                    action["_id"] = source["log_id"]
                    source["rowkey"] = source["log_id"] 
                    source = json.dumps(source,cls=MyEncoder, ensure_ascii=False) 
                    action["_source"] = source
                actions.append(action)
            bulk(es,actions,index="liuren",doc_type=tablename,chunk_size=2000)
            j = j + piliang_nums
            if j < data_num:
                print str(j) + " docs insert"
            else:
                print str(data_num) + " docs insert"
        endTime = time.time()
        costtime = endTime - startTime
        QPS = data_num / costtime
        print tablename + "表数据导入es成功！"
        print "cost time:" + str(endTime - startTime)
        print "total insert rows:", str(data_num)
        print "QPS:" + str(QPS)
    except Exception, e:
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
if __name__ == '__main__':  
    mysql_to_es()
    




