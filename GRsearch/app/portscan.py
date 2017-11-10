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

client = Elasticsearch("172.16.39.233:9200")

def search(request):
    search_content = request.GET.get('q', '')   
    page = int(request.GET.get("page", "1"))
    filter = request.GET.get('filter', '')
    current_page = page
    last_page = current_page - 1
    next_page = current_page + 1
    s_type = request.GET.get("s_type", "webscan")
    index_dict = {
                  "webscan": "scan",
                  "portscan": "portscan-2017.08.21",
                  "ipv4": "ipv4",
                  "waf": "liuren"
                  }
    if s_type == "webscan":  # 搜索webscan索引
        content = webscan(search_content, page, current_page, last_page, next_page, s_type, index_dict)   
        return render(request, 'fenye1.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"] })     
    else:
        if s_type == "portscan":  # 端口扫描portscan-2017.08.21
            if filter == "":
                if ":" in search_content:
                    if "AND" in search_content:
                        content = portscan_with_and(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                        return render(request, 'portscan.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"]
                                              })
                    elif "OR" in search_content:
                        content = portscan_with_or(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                        return render(request, 'portscan.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"]
                                              })
                    elif "NOT" in search_content:
                        content = portscan_with_not(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                        return render(request, 'portscan.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"]
                                              })
                    else:
                        content = portscan_with_field(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                        return render(request, 'portscan.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"]
                                              })
                else:
                    content = portscan_with_content(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                    return render(request, 'portscan.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"]
                                              })
            else:
                reg2 = re.compile(r'\s*:\s*')
                search_list = reg2.split(filter)
                filter_field = "location."+search_list[0]+".keyword"
                filter_field_value = search_list[1]
                if ":" in search_content:
                    if "AND" in search_content:
                        content = portscan_with_and_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                        return render(request, 'portscan_filter.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"],
                                             "filter": filter    
                                              })
                    elif "OR" in search_content:
                        content = portscan_with_or_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                        return render(request, 'portscan_filter.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"],
                                             "filter": filter    
                                              })
                    elif "NOT" in search_content:
                        content = portscan_with_not_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                        return render(request, 'portscan_filter.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"],
                                             "filter": filter    
                                              })
                    else:
                        content = portscan_with_field_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                        return render(request, 'portscan_filter.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"],
                                             "filter": filter    
                                              })
                else:
                    content = portscan_with_content_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                    return render(request, 'portscan_filter.html', {
                                             "all_hits":content["all_hits"],
                                             "search_content": content["search_content"],
                                             "total_nums":content["total_nums"],
                                             "time_took":content["time_took"],
                                             "page_nums":content["page_nums"],
                                             "current_page": content["current_page"],
                                             "last_page": content["last_page"],
                                             "next_page": content["next_page"],
                                             "page_list":content["page_list"],
                                             "s_type":content["s_type"],
                                             "filter": filter    
                                              })
                
                
        elif s_type == "ipv4":  # ipv4的内容
          if filter == "":
            es_list = ["es", "elasticsearch", "9200"]
            es_china = ["es china", "elasticsearch china", "9200 china"]
            if search_content in es_china:
                content = ipv4_es_china(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                return render(request, 'ipv4_es.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"]                                                        
                                               })
            else:
                if search_content in es_list:
                    content = ipv4_es(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                    return render(request, 'ipv4_es.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"]
                                                        
                                               })
                else:
                    if ":" in search_content:
                        if "AND" in search_content:
                            content = ipv4_with_and(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                            return render(request, 'ipv4.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"]
                                                        
                                               })
                        elif "OR" in search_content:
                            content = ipv4_with_or(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                            return render(request, 'ipv4.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"]
                                                        
                                               })
                        elif "NOT" in search_content:
                            content = ipv4_with_not(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                            return render(request, 'ipv4.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"]
                                               })
                        else :
                            content = ipv4_with_field(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                            return render(request, 'ipv4.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"]
                                               })
                    else:
                        content = ipv4_with_content(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                        return render(request, 'ipv4.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"]
                                               })
          else: #添加过滤条件的搜索
            es_list = ["es", "elasticsearch", "9200"]
            es_china = ["es china", "elasticsearch china", "9200 china"]
            reg2 = re.compile(r'\s*:\s*')
            search_list = reg2.split(filter)
            filter_field = "location."+search_list[0]+".raw"
            filter_field_value = search_list[1]
            if search_content in es_china:
                content = ipv4_es_china_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                return render(request, 'ipv4_es_filter.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"],
                                                        "filter": filter                                                       
                                               })
            else:
                if search_content in es_list:
                    content = ipv4_es_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                    return render(request, 'ipv4_es_filter.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"],
                                                        "filter": filter         
                                                        
                                               })
                else:
                    if ":" in search_content:
                        if "AND" in search_content:
                            content = ipv4_with_and_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                            return render(request, 'ipv4_filter.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"],
                                                        "filter": filter         
                                                        
                                               })
                        elif "OR" in search_content:
                            content = ipv4_with_or_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                            return render(request, 'ipv4_filter.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"],
                                                        "filter": filter         
                                                        
                                               })
                        elif "NOT" in search_content:
                            content = ipv4_with_not_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                            return render(request, 'ipv4_filter.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"],
                                                        "filter": filter         
                                               })
                        else :
                            content = ipv4_with_field_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                            return render(request, 'ipv4_filter.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"],
                                                        "filter": filter         
                                               })
                    else:
                        content = ipv4_with_content_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                        return render(request, 'ipv4_filter.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"],
                                                        "filter": filter         
                                               })
        elif s_type == "waf":
            if filter == "":
                content = waf_with_content(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                return render(request, 'waf.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"]
                                               })
            else:
                reg2 = re.compile(r'\s*:\s*')
                search_list = reg2.split(filter)
                filter_field = search_list[0]
                filter_field_value = search_list[1]
                content = waf_with_content_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value)
                return render(request, 'waf_filter.html', {
                                                        "all_hits":content["all_hits"],
                                                        "search_content": content["search_content"],
                                                        "total_nums":content["total_nums"],
                                                        "time_took":content["time_took"],
                                                        "page_nums":content["page_nums"],
                                                        "current_page": content["current_page"],
                                                        "last_page": content["last_page"],
                                                        "next_page": content["next_page"],
                                                        "page_list":content["page_list"],
                                                        "s_type":content["s_type"],
                                                        "filter": filter
                                               })
def webscan(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="t_engin_task_detail",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                             "match":{
                                                      "result": search_content
                                                      }
                                             },
                                   "highlight":{
                                                "pre_tags":['<span class="keyWord">'],
                                                "post_tags": ['</span>'],
                                                "fields":{
                                                          "result":{}
                                                          }
                                                }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        if "result" in hit["highlight"]:
            hit_dict["result"] = "".join(hit["highlight"]["result"])
        else:
            hit_dict["result"] = hit["_source"]["result"]
        hit_dict["site"] = hit["_source"]["site_url"]
        hit_dict["grade"] = hit["_source"]["grade"]
        hit_list.append(hit_dict)
    page_list = [
                i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
            ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type }
    return context
def portscan_with_content(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                             "match_phrase":{
                                                      "_all": search_content
                                                      }
                                             }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def portscan_with_field(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    reg2 = re.compile(r'\s*:\s*')
    search_list = reg2.split(search_content)
    field1 = search_list[0]
    field1_value = search_list[1]
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                             "match_phrase":{
                                                      field1: field1_value
                                                      }
                                             }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def portscan_with_not(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    reg1 = re.compile(r'\s+NOT\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ]
                                                 }
                                           }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def portscan_with_or(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    reg1 = re.compile(r'\s+OR\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "should": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                           }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def portscan_with_and(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    reg1 = re.compile(r'\s+AND\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                         }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def portscan_with_content_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               "_all" : search_content
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                }
                                            }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def portscan_with_field_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    reg2 = re.compile(r'\s*:\s*')
    search_list = reg2.split(search_content)
    field1 = search_list[0]
    field1_value = search_list[1]
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                }
                                            }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def portscan_with_not_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    reg1 = re.compile(r'\s+NOT\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                           }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def portscan_with_or_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    reg1 = re.compile(r'\s+OR\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "should": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                           }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def portscan_with_and_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    reg1 = re.compile(r'\s+AND\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                             "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("tags") == True:
            hit_dict["tags"] = hit["_source"]["tags"][0]
        else:
            hit_dict["tags"] = ""
        hit_list.append(hit_dict)
    page_list = [
                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_es_china(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="ipv4host",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                   {
                                                    "match": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    },
                                                    {
                                                       "match":{
                                                           "location.country": "china"
                                                         }
                                                      }
                                                     ]
                                                 }
                                         }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                         i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                         ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_es(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="ipv4host",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                   {
                                                    "match": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    }
                                                     ]
                                                 }
                                         }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                         i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                         ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_with_and(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    reg1 = re.compile(r'\s+AND\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                                 index=index_dict[s_type],
                                 doc_type="ipv4host",
                                 body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                         }
                                   }
                               )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                 i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                  ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_with_or(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    reg1 = re.compile(r'\s+OR\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                                index=index_dict[s_type],
                                doc_type="ipv4host",
                                body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "should": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                           }
                                      }
                                   )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                ]
    
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_with_not(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    reg1 = re.compile(r'\s+NOT\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                                index=index_dict[s_type],
                                doc_type="ipv4host",
                                body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ]
                                                 }
                                           }
                                      }
                                   )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_with_field(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    reg2 = re.compile(r'\s*:\s*')
    search_list = reg2.split(search_content)
    field1 = search_list[0]
    field1_value = search_list[1]
    response = client.search(
                                 index=index_dict[s_type],
                                 doc_type="ipv4host",
                                 body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "match": {
                                            field1: field1_value
                                                 }
                                         }
                                   }
                               )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                 i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                  ]
    
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context 
def ipv4_with_content(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    response = client.search(
                                index=index_dict[s_type],
                                doc_type="ipv4host",
                                body={
                                     "from": (page - 1) * 20,
                                     "size": 20,
                                     "query": {
                                        "match": {
                                            "_all": search_content
                                                 }
                                         }
                                      }
                                )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                 ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_es_china_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="ipv4host",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                   {
                                                    "match": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    },
                                                    {
                                                       "match":{
                                                           "location.country": "china"
                                                         }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                         i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                         ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_es_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="ipv4host",
                             body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                   {
                                                    "match": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         }
                                   }
                             )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                         i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                         ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_with_and_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    reg1 = re.compile(r'\s+AND\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                                 index=index_dict[s_type],
                                 doc_type="ipv4host",
                                 body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                             "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         }
                                   }
                               )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                 i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                  ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_with_or_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    reg1 = re.compile(r'\s+OR\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                                index=index_dict[s_type],
                                doc_type="ipv4host",
                                body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "should": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                           }
                                      }
                                   )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                ]
    
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_with_not_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    reg1 = re.compile(r'\s+NOT\s+')  # 分割查询语句
    search_list = reg1.split(search_content)
    reg2 = re.compile(r'\s*:\s*')
    search_1_list = reg2.split(search_list[0])
    search_2_list = reg2.split(search_list[1])
    field1 = search_1_list[0]
    field1_value = search_1_list[1]
    field2 = search_2_list[0]
    field2_value = search_2_list[1]
    response = client.search(
                                index=index_dict[s_type],
                                doc_type="ipv4host",
                                body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                           }
                                      }
                                   )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                    i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context
def ipv4_with_field_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    reg2 = re.compile(r'\s*:\s*')
    search_list = reg2.split(search_content)
    field1 = search_list[0]
    field1_value = search_list[1]
    response = client.search(
                                 index=index_dict[s_type],
                                 doc_type="ipv4host",
                                 body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                }
                                            }  
                                       }
                               )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                 i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                  ]
    
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context 
def ipv4_with_content_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter_field, filter_field_value):
    response = client.search(
                                index=index_dict[s_type],
                                doc_type="ipv4host",
                                body={
                                     "from": (page - 1) * 20,
                                     "size": 20,
                                     "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               "_all" : search_content
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                }
                                            }
                                      }
                                )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        hit_dict["id"] = hit["_id"]
        if hit["_source"].has_key("ip") == True:
            hit_dict["ip"] = hit["_source"]["ip"]
        else:
            hit_dict["ip"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("country") == True:
                hit_dict["country_code"] = hit["_source"]["location"]["country_code"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
            else:
                hit_dict["country"] = ""
        else:
            hit_dict["country"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("province") == True:
                hit_dict["province"] = hit["_source"]["location"]["province"]
            else:
                hit_dict["province"] = ""
        else:
            hit_dict["province"] = ""
        if hit["_source"].has_key("location") == True:
            if hit["_source"]["location"].has_key("city") == True:
                hit_dict["city"] = hit["_source"]["location"]["city"]
            else:
                hit_dict["city"] = ""
        else:
            hit_dict["city"] = ""
        if hit["_source"].has_key("updated_at") == True:
            hit_dict["update_time"] = hit["_source"]["updated_at"]
        else :
            hit_dict["update_time"] = ""
        hit_list.append(hit_dict)
    page_list = [
                                i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                                 ]
    context = {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": current_page,
                                             "last_page": last_page,
                                             "next_page": next_page,
                                             "page_list":page_list,
                                             "s_type":s_type
                                              }
    return context  
def aggs(request):
    search_content = request.GET.get('q', '')
    # search_content = request.POST
    es_list = ["es", "elasticsearch", "9200"]
    es_china = ["es china", "elasticsearch china", "9200 china"]
    if search_content in es_china:
        aggs = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                        {
                                        "match": {
                                                "9200.http.get.headers.content_type": "json"
                                                }
                                        },
                                        {
                                            "match_phrase": {
                                                "9200.http.get.body": "You Know, for Search"
                                                    }
                                               },
                                         {
                                          "match": {
                                                    "location.city": "china"
                                                    }
                                          }
                                        ]
                                    }
                                  },
                        "aggs": {
                            "country": {
                                "terms": {
                                    "field": "location.country.raw",
                                    "size": 10,
                                    "shard_size": 1000
                                        }
                                    },
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 10,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 10,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        country_list = []
        for bucket in aggs["aggregations"]["country"]["buckets"]:
            country_dict = {}
            country_dict["country_name"] = bucket["key"]
            country_dict["count"] = bucket["doc_count"]
            country_list.append(country_dict)
        province_list = []
        for bucket in aggs["aggregations"]["province"]["buckets"]:
            province_dict = {}
            province_dict["province_name"] = bucket["key"]
            province_dict["count"] = bucket["doc_count"]
            province_list.append(province_dict)    
        city_list = []
        for bucket in aggs["aggregations"]["city"]["buckets"]:
            city_dict = {}
            city_dict["city_name"] = bucket["key"]
            city_dict["count"] = bucket["doc_count"]
            city_list.append(city_dict)
        aggs_content = {}
        aggs_content["country_list"] = country_list
        aggs_content["province_list"] = province_list
        aggs_content["city_list"] = city_list
        result = json.dumps(aggs_content)
        return HttpResponse(result)
    elif search_content in es_list:
        aggs = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                        {
                                        "match": {
                                                "9200.http.get.headers.content_type": "json"
                                                }
                                        },
                                        {
                                            "match_phrase": {
                                                "9200.http.get.body": "You Know, for Search"
                                                    }
                                               }
                                        ]
                                    }
                                  },
                        "aggs": {
                            "country": {
                                "terms": {
                                    "field": "location.country.raw",
                                    "size": 10,
                                    "shard_size": 1000
                                        }
                                    },
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 10,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 10,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        country_list = []
        for bucket in aggs["aggregations"]["country"]["buckets"]:
            country_dict = {}
            country_dict["country_name"] = bucket["key"]
            country_dict["count"] = bucket["doc_count"]
            country_list.append(country_dict)
        province_list = []
        for bucket in aggs["aggregations"]["province"]["buckets"]:
            province_dict = {}
            province_dict["province_name"] = bucket["key"]
            province_dict["count"] = bucket["doc_count"]
            province_list.append(province_dict)    
        city_list = []
        for bucket in aggs["aggregations"]["city"]["buckets"]:
            city_dict = {}
            city_dict["city_name"] = bucket["key"]
            city_dict["count"] = bucket["doc_count"]
            city_list.append(city_dict)
        aggs_content = {}
        aggs_content["country_list"] = country_list
        aggs_content["province_list"] = province_list
        aggs_content["city_list"] = city_list
        result = json.dumps(aggs_content)
        return HttpResponse(result)
    else:
        aggs = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                        {
                                        "match": {
                                                "_all": search_content
                                                }
                                        }
                                        ]
                                    }
                                  },
                        "aggs": {
                            "country": {
                                "terms": {
                                    "field": "location.country.raw",
                                    "size": 10,
                                    "shard_size": 1000
                                        }
                                    },
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 10,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 10,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        country_list = []
        for bucket in aggs["aggregations"]["country"]["buckets"]:
            country_dict = {}
            country_dict["country_name"] = bucket["key"]
            country_dict["count"] = bucket["doc_count"]
            country_list.append(country_dict)
        province_list = []
        for bucket in aggs["aggregations"]["province"]["buckets"]:
            province_dict = {}
            province_dict["province_name"] = bucket["key"]
            province_dict["count"] = bucket["doc_count"]
            province_list.append(province_dict)    
        city_list = []
        for bucket in aggs["aggregations"]["city"]["buckets"]:
            city_dict = {}
            city_dict["city_name"] = bucket["key"]
            city_dict["count"] = bucket["doc_count"]
            city_list.append(city_dict)
        aggs_content = {}
        aggs_content["country_list"] = country_list
        aggs_content["province_list"] = province_list
        aggs_content["city_list"] = city_list
        result = json.dumps(aggs_content)
        return HttpResponse(result)
    
