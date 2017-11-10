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


def test():
        client = Elasticsearch("172.16.39.233:9200")
        search_content = "xss"
        filter = "org_name.keyword:宁德数字宁德建设办公室"
        reg2 = re.compile(r'\s*:\s*')
        search_list = reg2.split(filter)
        filter_field = search_list[0]
        filter_field_value = search_list[1]
        aggs = client.search(
                index="liuren",
                doc_type="waf_log",
                body={
                      "size": 0,
                      "query": {
                                        "bool":{
                                            "must":[{
                                              "match": {
                                                  "_all": search_content
                                                 }
                                                  }],
                                            "filter":{
                                                  "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                  }
                                               }
                                            },
                      "aggs":{
                            "org":{
                                   "terms":{
                                        "field": "org_name.keyword",
                                        "size": 10,
                                        "shard_size": 1000
                                            }
                                   },
                            "site":{
                                    "terms":{
                                        "field": "site_url.keyword",
                                        "size": 10,
                                        "shard_size": 1000
                                             }
                                    },
                            "event":{
                                     "terms":{
                                        "field": "type_name.keyword",
                                        "size": 10,
                                        "shard_size": 1000
                                              }
                                     }
                              }
                      }
                )
        print aggs
        org_list = []
        for bucket in aggs["aggregations"]["org"]["buckets"]: 
            org_dict = {}
            org_dict["name"] = bucket["key"]
            org_dict["value"] = bucket["doc_count"]
            org_list.append(org_dict)
        site_list = []
        for bucket in aggs["aggregations"]["site"]["buckets"]:
            site_dict = {}
            site_dict["name"] = bucket["key"]
            site_dict["value"] = bucket["doc_count"]
            site_list.append(site_dict)
        event_list = []
        for bucket in aggs["aggregations"]["event"]["buckets"]:
            event_dict = {}
            event_dict["name"] = bucket["key"]
            event_dict["value"] = bucket["doc_count"]
            event_list.append(event_dict)
        aggs_content = {}
        aggs_content["org_list"] = org_list
        aggs_content["site_list"] = site_list
        aggs_content["event_list"] = event_list
        result = json.dumps(aggs_content)
        print result
        
if __name__ == '__main__':
    test()