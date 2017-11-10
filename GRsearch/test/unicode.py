# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
from elasticsearch import Elasticsearch

client = Elasticsearch("172.16.39.233:9200")

def waf_aggs():
    search_content = "xss"
    filter = ""
    org_dict = {
                 "福建省发改委" : [119.303633, 26.099065],
                 "宁德数字宁德建设办公室" : [119.532834, 26.673602],
                 "莆田市信息中心" : [119.006812, 25.440215],
                 "大田县人民政府" : [117.853597, 25.699028],
                 "龙岩市数字龙岩建设办公室" : [117.023678, 25.081386],
                 "东山县政府办" : [117.432811, 23.71112],
                 "城厢区人民政府" : [119.000808, 25.424802],
                 "泉州市数字泉州建设办公室" : [118.682996, 24.876104],
                 "龙岩数字办" : [117.023678, 25.081386],
                 "福州市“数字福州”建设领导小组办公室" : [119.302813, 26.080522],
                 "福建省经济和信息化委员会" : [119.357676, 26.045975],
                 "连城县人民政府办公室" : [116.760731, 25.716959],
                 "南平数字办" : [118.184413, 26.647573],
                 "龙岩市供销社" : [117.029801, 25.081676],
                 "沙县公安局" : [117.80119, 26.397623],
                 "莆田市卫生计生委" : [119.025098, 25.449127],
                 "福建永安市公安局" : [117.371148, 25.982532],
                 "宁德市新媒体网络传媒有限公司" : [119.529877, 26.66964]
                 }
    org_dict = json.dumps(org_dict,encoding='UTF-8', ensure_ascii=False)
    org_dict = json.loads(org_dict)
    print org_dict
    if filter == "":
        aggs = client.search(
                index="liuren",
                doc_type="waf_log",
                body={
                      "size": 0,
                      "query": {
                                "match_phrase": {
                                    "_all": search_content
                                          }
                                },
                      "aggs":{
                            "map":{
                                "terms":{
                                    "field": "src_location.keyword",
                                    "size": 10000,
                                    "shard_size": 1000
                                        },
                                "aggs":{
                                    "zuobiao":{
                                        "terms": {
                                            "field": "src_coordinate.keyword"   
                                                }
                                               }
                                        }
                                   },
                            "attack":{
                                "terms":{
                                    "field": "org_name.keyword",
                                    "size": 20,
                                    "shard_size": 50
                                         },
                                "aggs":{
                                    "src":{
                                        "terms":{
                                            "field": "src_location.keyword",
                                            "size": 10,
                                            "shard_size": 700
                                                 }
                                           }
                                        }     
                                    }
                              }
                      }
                )
        zuobiao_dict = {}
        for bucket in aggs["aggregations"]["map"]["buckets"]:
            zuobiao = []
            key = bucket["key"]
            content = bucket["zuobiao"]["buckets"][0]["key"] 
            if content != "":
                reg = re.compile(r'\s*,\s*')
                zuobiao_list = reg.split(content)
                zuobiao.append(float(zuobiao_list[1]))
                zuobiao.append(float(zuobiao_list[0]))  
                zuobiao_dict[key] = zuobiao
        zuobiao_dict = dict(org_dict.items()+zuobiao_dict.items())
        zuobiao_dict = json.dumps(zuobiao_dict,ensure_ascii=False)
        line_list = []
        dest_list = []
        for bucket in aggs["aggregations"]["attack"]["buckets"]:
            dest_dict = {}
            dest_dict["name"] = bucket["key"]
            dest_dict["value"] = bucket["doc_count"]
            dest_dict = json.dumps(dest_dict,ensure_ascii=False)
            dest_list.append(dest_dict)
            for bucket1 in bucket["src"]["buckets"]:
                action = []
                src_dict = {}
                src_dict["name"] = bucket1["key"]
                src_dict = json.dumps(src_dict,ensure_ascii=False)
                action.append(src_dict)
                action.append(dest_dict)
                line_list.append(action)
        line_list = json.dumps(line_list,ensure_ascii=False)
        line_list = line_list.replace('"{','{')
        line_list = line_list.replace('}"','}')
        line_list = line_list.replace('\\"','"')
        print line_list
        aggs_content = {}
        aggs_content["zuobiao_dict"] = zuobiao_dict
        aggs_content["line_list"] = line_list
        aggs_content["dest_list"] = dest_list
        print aggs_content["line_list"]
    else:
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
                                              "match_phrase": {
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
                            "map":{
                                "terms":{
                                    "field": "src_location.keyword",
                                    "size": 10000,
                                    "shard_size": 1000
                                        },
                                "aggs":{
                                    "zuobiao":{
                                        "terms": {
                                            "field": "src_coordinate.keyword"   
                                                }
                                               }
                                        }
                                   },
                            "attack":{
                                "terms":{
                                    "field": "org_name.keyword",
                                    "size": 1,
                                    "shard_size": 50
                                         },
                                "aggs":{
                                    "src":{
                                        "terms":{
                                            "field": "src_location.keyword",
                                            "size": 10,
                                            "shard_size": 700
                                                 }
                                           }
                                        }     
                                    }
                              }
                      }
                )
        zuobiao_dict = {}
        for bucket in aggs["aggregations"]["map"]["buckets"]:
            zuobiao = []
            key = bucket["key"]
            content = bucket["zuobiao"]["buckets"][0]["key"] 
            if content != "":
                reg = re.compile(r'\s*,\s*')
                zuobiao_list = reg.split(content)
                zuobiao.append(float(zuobiao_list[1]))
                zuobiao.append(float(zuobiao_list[0]))  
                zuobiao_dict[key] = zuobiao
        zuobiao_dict = dict(org_dict.items()+zuobiao_dict.items())
        zuobiao_dict = json.dumps(zuobiao_dict, ensure_ascii = False)
        line_list = []
        dest_list = []
        for bucket in aggs["aggregations"]["attack"]["buckets"]:
            dest_dict = {}
            dest_dict["name"] = bucket["key"]
            dest_dict["value"] = bucket["doc_count"]
            dest_dict = json.dumps(dest_dict)
            dest_list.append(dest_dict)
            for bucket1 in bucket["src"]["buckets"]:
                action = []
                src_dict = {}
                src_dict["name"] = bucket1["key"]
                src_dict = json.dumps(src_dict)
                action.append(src_dict)
                action.append(dest_dict)
                line_list.append(action)
        
        
if __name__ == '__main__':
    waf_aggs()