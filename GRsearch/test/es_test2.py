# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
from elasticsearch import Elasticsearch
from thrift import Thrift  
from thrift.transport import TSocket, TTransport  
from thrift.protocol import TBinaryProtocol  
from hbase import ttypes  
from hbase import Hbase
from hbase.Hbase import * 


client = Elasticsearch(hosts=["172.16.39.231","172.16.39.232","172.16.39.233","172.16.39.234"],timeout=5000)
response = client.search(
                    index="fj_tsgz",
                    doc_type= "w_wel_warning",
                    body = {
                             "stored_fields": "rowkey",
                             "query":{
                                 "range":{
                                    "date":{
                                       "gte":"2017-11-02"     
                                            }     
                                        }    
                                    }       
                            }         
                        )
print response