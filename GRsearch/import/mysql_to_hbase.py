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



def mysqltohbase():
    transport = TSocket.TSocket('172.16.39.231', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Client(protocol)
    transport.open()
    tablename = raw_input("表：")
#     contents = ColumnDescriptor(name='message:', maxVersions=1)
#     client.createTable(tablename, [contents])
    conn = MySQLdb.connect(host='172.16.39.180', user='webscan', passwd='1qaz2wsx', db='liuren', port=3306, charset='utf8')
    cur = conn.cursor()
    piliang_nums = 500
    startTime = time.time()
    try:
        sql1 = "SELECT COLUMN_NAME FROM information_schema.COLUMNS where TABLE_SCHEMA = 'liuren' and TABLE_NAME = '" + tablename + "'"
        num_of_fields = cur.execute(sql1)
        data1 = cur.fetchall()
        a = 0
        listfield = []
        while a < num_of_fields:
            if data1[a][0] == "log_id":
                fieldnum = a
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
            mutationsBatch = []
            for row in data:
                if row != None:
                    m = 0
                    mutations = []
                    while m < num_of_fields: 
                        content = str(row[m])
                        format_column = "message:" + listfield[m]
                        mutations.append(Mutation(column=format_column, value=content.encode('utf-8')))
                        m = m + 1    
                    mutationsBatch.append(Hbase.BatchMutation(row=str(row[fieldnum]), mutations=mutations))   
            if(len(mutationsBatch) > 0):
                client.mutateRows(tablename, mutationsBatch)   
            j = j + piliang_nums
            if j < data_num:
                print str(j) + " docs insert"
            else:
                print str(data_num) + " docs insert"
        endTime = time.time()
        costtime = endTime - startTime
        QPS = data_num / costtime
        print tablename + "表数据导入hbase成功！"
        print "cost time:" + str(endTime - startTime)
        print "total insert rows:", str(data_num)
        print "QPS:" + str(QPS)
    except Exception, e:
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
if __name__ == '__main__':  
    mysqltohbase()
    




