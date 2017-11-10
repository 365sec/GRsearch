#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import json
import urllib2
import traceback
import time
from datetime import date, datetime
from thrift import Thrift  
from thrift.transport import TSocket, TTransport  
from thrift.protocol import TBinaryProtocol  
from hbase import ttypes  
from hbase import Hbase
from hbase.Hbase import *  
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


def mysqltohbase():
    transport = TSocket.TSocket('172.16.39.234', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Client(protocol)
    transport.open()
    tablename = "waf_log"
#     database = raw_input("数据库:")
#     tablename = raw_input("表名:")
    conn = MySQLdb.connect(host='172.16.39.180', user='webscan', passwd='1qaz2wsx', db='liuren', port=3306, charset='utf8')
    cur = conn.cursor()
    piliang_nums = 1000
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
        j = 1221000
        while j < data_num:
            sql3 = "select * from " + tablename + " limit " + str(j) + "," + str(piliang_nums)
            cur.execute(sql3)
            data = cur.fetchall()
            actions = []
            mutationsBatch = []
            i = 1
            for row in data:
                if row != None:
                    n = i + j
                    m = 0
                    source = {}
                    action = {
                          "_id": n    
                              }
                    mutations = []
                    while m < num_of_fields: 
                        content = str(row[m])
                        source[listfield[m]] = row[m]
                        format_column = "message:" + listfield[m]
                        mutations.append(Mutation(column=format_column, value=content.encode('utf-8')))
                        m = m + 1  # 之后要做的是考虑source如何生成的问题，用到字典中的追加内容   
                    source["rowkey"] = n   
                    action["_source"] = source
                    mutationsBatch.append(Hbase.BatchMutation(row=str(n), mutations=mutations)) 
                i += 1   
                actions.append(action)
                if(len(mutationsBatch) == 100):
                    client.mutateRows("waf_logs", mutationsBatch)
                    mutationsBatch = []  
            bulk(es,actions,index="liurentest",doc_type="waf_log",chunk_size=2000)
            if(len(mutationsBatch) > 0):
                client.mutateRows("waf_logs", mutationsBatch)   
            j = j + piliang_nums
            print str(n) + " docs insert"
        endTime = time.time()
        costtime = endTime - startTime
        QPS = (n - 1) / costtime
        print tablename + "表数据导入hbase成功！"
        print "cost time:" + str(endTime - startTime)
        print "total insert rows:", str(n)
        print "QPS:" + str(QPS)
    except Exception, e:
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
if __name__ == '__main__':  
    mysqltohbase()
    




