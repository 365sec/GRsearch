# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
import time
from elasticsearch import Elasticsearch
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from django.shortcuts import render, HttpResponse
from hbase import Hbase
from hbase.ttypes import *


def test(search_content):
    client = Elasticsearch("172.16.39.233:9200")
    response = client.search(
                                index="liuren",
                                doc_type="waf_log",
                                body={
                                     "size": 10,
                                     "stored_fields": ["rowkey"],
                                     "query": {
                                        "match": {
                                            "_all": search_content
                                                 }
                                         }
                                      }
                                )
    total_nums = response["hits"]["total"]
#     time_took = float(response["took"]) / 1000
    hit_list = []
    rowkey_list = []
    for hit in response["hits"]["hits"]:
        rowkey_list.append(hit["fields"]["rowkey"][0])
    transport = TSocket.TSocket('172.16.39.234', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    hbase_client = Hbase.Client(protocol)
    transport.open()
    i = 0
    all_hits = []
    print rowkey_list
    while i < len(rowkey_list):
        result = hbase_client.getRow('waf_log', str(rowkey_list[i]))
        print result
        hit = {}
        for r in result:
            for key in r.columns.keys():
                reg = re.compile(r'\s*:\s*')
                key_content_list = reg.split(key)   #hbase中key的内容是message:field的形式
                hit[key_content_list[1]] = r.columns.get(key).value   #未做出错处理
        hit = json.dumps(hit,ensure_ascii=False)
        print hit
        all_hits.append(hit)
        i +=1
    print  all_hits 
if __name__ == '__main__':
    test("福")