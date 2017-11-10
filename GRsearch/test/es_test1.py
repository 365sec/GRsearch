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


def tsgz():
    client = Elasticsearch(hosts=["172.16.39.231","172.16.39.232","172.16.39.233","172.16.39.234"],timeout=5000)
    transport = TSocket.TSocket('172.16.39.231', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    hbase_client = Hbase.Client(protocol)
    transport.open()
    all_hits = t_wel_attack_real(client,hbase_client)
    print all_hits
    
def t_wel_attack_real(client,hbase_client): #实时攻击情况
    response = client.search(
                    index="fj_tsgz",
                    doc_type= "t_wel_website",
                    body = {
                             "stored_fields": "rowkey",
                             "query":{
                                 "range":{
                                    "date":{
                                       "gte":"2017-11-03"     
                                            }     
                                        }    
                                    }       
                            }         
                        )
    rowkey_list = []
    for hit in response["hits"]["hits"]:
        rowkey_list.append(hit["fields"]["rowkey"][0])
    all_hits = []
    i = 0
    while i < len(rowkey_list):
        result = hbase_client.getRow('t_wel_website', str(rowkey_list[i]))
        hit = {}
        for r in result:
            for key in r.columns.keys():
                reg = re.compile(r'\s*:\s*')
                key_content_list = reg.split(key)   #hbase中key的内容是message:field的形式
                if key_content_list[1] =="type":
                    if r.columns.get(key).value == "0":
                        hit[key_content_list[1]] = "一级网站"
                    else:
                        hit[key_content_list[1]] = "二级网站"
                else:
                    hit[key_content_list[1]] = r.columns.get(key).value   #未做出错处理
            hit = json.dumps(hit,encoding="utf-8",ensure_ascii=False)
            hit = json.loads(hit)
        hit["rowkey"] = rowkey_list[i]
        all_hits.append(hit)
        i +=1
    return all_hits

def t_wel_attack_today(request):
    print ""

def t_wel_company(request):
    print ""
    
def t_wel_company_total(request):
    print ""      
      
def t_wel_darknet():  #暗网统计数据
    print ""
    
def t_wel_event():    #事件统计
    print ""

def t_wel_event_area(client):  #分地区事件统计
    response = client.search(
                 index="fj_tsgz",
                 doc_type="t_wel_event_area",
                 body={
                    "size":0,
                    "aggs":{
                        "num":{
                            "terms":{
                                "field": "city.keyword",
                                "shard_size": 100,
                                "order": {
                                    "SUM": "desc"      
                                          }
                                     },
                            "aggs":{
                                 "SUM":{
                                     "sum":{
                                         "field":"count"   
                                            }   
                                        }    
                                    }   
                               }    
                            }
                       }
                    )
    #这里的数据库内容没明确

def t_wel_jc(client):    #各家贡献数据量
    response = client.search(
                 index="fj_tsgz",
                 doc_type="t_wel_jc",
                 body={
                    "size":0,
                    "aggs":{
                        "company":{
                            "terms":{
                                "field": "company.keyword"
                                     },
                            "aggs":{
                                 "SUM":{
                                     "sum":{
                                         "field":"count"   
                                            }   
                                        },
                                 "TYPE":{
                                     "terms":{
                                         "field": "type.keyword"     
                                              },
                                     "aggs":{
                                         "sum1":{
                                             "sum":{
                                                 "field": "count"   
                                                    }    
                                                 }      
                                             }    
                                    }}   
                               }    
                            }
                       }
                    )
    company_list = []
    for bucket in response["aggregations"]["company"]["buckets"]:
        company_dict = {}
        if bucket["key"] == "0":
            company_dict["company"] = "国瑞信安"
        elif bucket["key"] == "1":
            company_dict["company"] = "美亚"
        elif bucket["key"] == "2":
            company_dict["company"] = "360"
        elif bucket["key"] == "3":
            company_dict["company"] = "云盾"
        elif bucket["key"] == "4":
            company_dict["company"] = "永信"
        else:
            company_dict["company"] = "六壬"
        company_dict = json.dumps(company_dict,encoding="utf-8",ensure_ascii=False)
        company_dict = json.loads(company_dict)
        company_dict["count"] = int(bucket["SUM"]["value"])
        type_list = []
        for content in bucket["TYPE"]["buckets"]:
            type_dict = {}
            type_dict["type"] = content["key"]
            type_dict["count"] = int(content["sum1"]["value"])
            type_list.append(type_dict)
        company_dict["type_list"] = type_list
        company_list.append(company_dict)
    return company_list

def t_wel_map(client):  #攻击图
    dest_dict = {
                   "厦门" : [118.11022,24.490474],
                   "福州" : [119.306239,26.075302]
                 }
    dest_dict = json.dumps(dest_dict,encoding="utf-8",ensure_ascii=False)
    dest_dict = json.loads(dest_dict)
    response = client.search(
                  index = "fj_tsgz",
                  doc_type = "t_wel_map",
                  body = {                          
                           "size": 0,
                           "aggs": {
                             "attack":{
                               "terms": {
                                 "field": "from.keyword",
                                 "size": 1000,
                                 "shard_size": 1000
                               },
                               "aggs": {
                                 "dest": {
                                   "terms": {
                                     "field": "to.keyword",
                                     "size": 10,
                                     "shard_size": 10
                                   }
                                 }
                               }
                             },
                             "zuobiao": {
                               "terms": {
                                 "field": "from.keyword",
                                 "size": 1000,
                                 "shard_size": 1000
                               },
                               "aggs": {
                                 "agg2": {
                                   "terms": {
                                     "field": "from_x.keyword",
                                     "size": 1
                                   },
                                   "aggs": {
                                     "agg3": {
                                       "terms": {
                                         "field": "from_y.keyword",
                                         "size": 1
                                       }
                                     }
                                   }
                                 }
                               }
                             }
                           }
                         }
                       )
    attack_num = int(response["hits"]["total"])
    zuobiao_dict = {}
    for bucket in response["aggregations"]["zuobiao"]["buckets"]:
        zuobiao = []
        zuobiao.append(float(bucket["agg2"]["buckets"][0]["key"]))
        zuobiao.append(float(bucket["agg2"]["buckets"][0]["agg3"]["buckets"][0]["key"]))
        key = bucket["key"]
        zuobiao_dict[key] = zuobiao
    zuobiao_dict = dict(dest_dict.items()+zuobiao_dict.items())
    zuobiao_dict = json.dumps(zuobiao_dict,ensure_ascii=False)
    line_list = []
    dest_list = [
                 {"name":"厦门"},
                 {"name":"福州"}
                 ]
    dest_list = json.dumps(dest_list,encoding="utf-8",ensure_ascii=False)
    for bucket in response["aggregations"]["attack"]["buckets"]:
        src_dict = {}
        src_dict["name"] = bucket["key"]
        src_dict = json.dumps(src_dict,ensure_ascii=False)
        for bucket1 in bucket["dest"]["buckets"]:
            action = []
            dest_dict = {}
            dest_dict["name"] = bucket1["key"]
            dest_dict = json.dumps(dest_dict,ensure_ascii=False)
            action.append(src_dict)
            action.append(dest_dict)
            line_list.append(action)
    line_list = json.dumps(line_list,ensure_ascii=False)
    line_list = line_list.replace('"{','{')
    line_list = line_list.replace('}"','}')
    line_list = line_list.replace('\\"','"')
    map_dict = {}
    map_dict["line_list"] = line_list
    map_dict["dest_list"] = dest_list
    map_dict["zuobiao_dict"] = zuobiao_dict
    map_dict["attack_num"] = attack_num
    return map_dict
def t_wel_rec(client):   #等保数据
    response = client.search(
                  index = "fj_tsgz",
                  doc_type = "t_wel_rec",
                  body = {
                    "size": 0,
                    "aggs": {
                      "agg1": {
                        "terms": {
                          "field": "city.keyword",
                          "size": 100,
                          "shard_size": 100
                        },
                        "aggs": {
                          "unit_num": {
                            "sum": {
                              "field": "unit"
                            }
                          },
                          "site_num":{
                            "sum": {
                              "field": "site"
                            }
                          },
                          "system_num":{
                            "sum": {
                              "field": "system"
                            }
                          },
                          "point_num":{
                            "sum": {
                              "field": "point"
                            }
                          },
                          "nonpoint_num":{
                            "sum": {
                              "field": "nonpoint"
                            }
                          }
                        }
                      },
                      "unit_sum":{
                        "sum_bucket": {
                          "buckets_path": "agg1.unit_num"
                        }
                      },
                      "site_sum":{
                        "sum_bucket": {
                          "buckets_path": "agg1.site_num"
                        }
                      },
                      "system_sum":{
                        "sum_bucket": {
                          "buckets_path": "agg1.system_num"
                        }
                      },
                      "point_sum":{
                        "sum_bucket": {
                          "buckets_path": "agg1.point_num"
                        }
                      },
                      "nonpoint_sum":{
                        "sum_bucket": {
                          "buckets_path": "agg1.nonpoint_num"
                        }
                      }
                    }
                  }
                )
    rec_list = []
    for bucket in response["aggregations"]["agg1"]["buckets"]:
        rec_dict = {}
        rec_dict["name"]= bucket["key"]
        rec_dict["unit"]= bucket["unit_num"]["value"]
        rec_dict["site"]= bucket["site_num"]["value"]
        rec_dict["system"]= bucket["system_num"]["value"]
        rec_dict["point"]= bucket["point_num"]["value"]
        rec_dict["nonpoint"]= bucket["nonpoint_num"]["value"]
        rec_list.append(rec_dict)
    rec_province_dict = {}
    rec_province_dict["name"]="福建省"
    rec_province_dict["unit"]=response["aggregations"]["unit_sum"]["value"]
    rec_province_dict["site"]=response["aggregations"]["site_sum"]["value"]
    rec_province_dict["system"]=response["aggregations"]["system_sum"]["value"]
    rec_province_dict["point"]=response["aggregations"]["point_sum"]["value"]
    rec_province_dict["nonpoint"]=response["aggregations"]["nonpoint_sum"]["value"]
    rec_province_dict = json.dumps(rec_province_dict,encoding="utf-8",ensure_ascii=False)
    rec_province_dict = json.loads(rec_province_dict)   #转码
    rec_list.append(rec_province_dict)
    return rec_list

def t_wel_top():   #风险排名
    print ""

def t_wel_warning():  #告警信息
    print ""

def t_wel_website():   #网站风险分布
    print ""
if __name__ == "__main__":
    tsgz()











