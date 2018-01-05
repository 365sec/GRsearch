# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
import urllib2
import time
import ConfigParser
from elasticsearch import Elasticsearch
from django.shortcuts import render, HttpResponse
import os
import logging


logger = logging.getLogger("ip")
conf = ConfigParser.ConfigParser()
conf.read(os.path.join(os.path.dirname(__file__),"..","TSsearch"))
str_es_hosts = conf.get("elasticsearch", "hosts")
print str_es_hosts
es_hosts = json.loads(str_es_hosts)
es_timeout = int(conf.get("elasticsearch", "timeout"))
client = Elasticsearch(hosts=es_hosts,timeout=es_timeout)

def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%dT%H:%M:%S", local_time)
    data_secs = (ct - long(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp


def search(request):
    search_content = request.GET.get('q', '')   
    page = int(request.GET.get("page", "1"))
    filter = request.GET.get('filter', '')
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR'] 
    #访问日志
    if filter != "":
        filter_log = "["
        for dict in json.loads(filter):
            if dict != "":
                filter_log += dict["filter"]+","
        filter_log_content = filter_log[:-1]
        filter_log_content += "]"
        print filter_log
        log_content = str(ip)+" ["+ get_time_stamp()+"+0800] \""+ search_content+"\" "+"\""+filter_log_content+"\""
    else:
        log_content = str(ip)+" ["+ get_time_stamp()+"+0800] \""+ search_content+"\" "+"\"\""
    logger.info(log_content)
    current_page = page
    last_page = current_page - 1
    next_page = current_page + 1
    s_type = request.GET.get("s_type", "ipv4")
    index_dict = {
                  "ipv4": "ipv4",
                  "websites": "websites1"
                  }
    if s_type == "ipv4":  # 搜索webscan索引
          if filter == "":
            es_list = ["es", "elasticsearch", "9200"]
            es_china = ["es china", "elasticsearch china", "9200 china"]
            if search_content in es_china:
                content = ipv4_es_china(search_content, page, current_page, last_page, next_page, s_type, index_dict)
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
                                                        "s_type":content["s_type"],
                                                        "filter": "[]"                          
                                               })
            else:
                if search_content in es_list:
                    content = ipv4_es(search_content, page, current_page, last_page, next_page, s_type, index_dict)
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
                                                        "s_type":content["s_type"],
                                                        "filter": "[]"         
                                                        
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
                                                        "s_type":content["s_type"],
                                                        "filter": "[]"         
                                                        
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
                                                        "s_type":content["s_type"],
                                                        "filter": "[]"         
                                                        
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
                                                        "s_type":content["s_type"],
                                                        "filter": "[]"         
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
                                                        "s_type":content["s_type"],
                                                        "filter": "[]"         
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
                                                        "s_type":content["s_type"],
                                                        "filter": "[]"         
                                               })
          else: #添加过滤条件的搜索
            es_list = ["es", "elasticsearch", "9200"]
            es_china = ["es china", "elasticsearch china", "9200 china"]
            field_dict = {
                          "全文" : "_all",
                          "ip" : "ip",
                          "国家/地区" : "location.country",
                          "省份" : "location.province",
                          "城市" : "location.city",
                          "updated_at" : "updated_at",
                          "端口协议" : "protocols"
                          }
            field_dict = json.dumps(field_dict)
            field_dict = json.loads(field_dict)
            if search_content in es_china:
                content = ipv4_es_china_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
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
                                                        "s_type":content["s_type"],
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)                                                     
                                               })
            else:
                if search_content in es_list:
                    content = ipv4_es_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
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
                                                        "s_type":content["s_type"],
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)        
                                                        
                                               })
                else:
                    if ":" in search_content:
                        if "AND" in search_content:
                            content = ipv4_with_and_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
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
                                                        "s_type":content["s_type"],
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)           
                                                        
                                               })
                        elif "OR" in search_content:
                            content = ipv4_with_or_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
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
                                                        "s_type":content["s_type"],
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)           
                                                        
                                               })
                        elif "NOT" in search_content:
                            content = ipv4_with_not_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
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
                                                        "s_type":content["s_type"],
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)           
                                               })
                        else :
                            content = ipv4_with_field_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
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
                                                        "s_type":content["s_type"],
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)           
                                               })
                    else:
                        content = ipv4_with_content_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
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
                                                        "s_type":content["s_type"],
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)           
                                               })
    elif s_type == "websites":
        if filter == "":
            if ":" in search_content:
                if "AND" in search_content:
                    content = websites_with_and(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                    return render(request, 'websites.html', {
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
                                                        "filter": "[]" 
                                                        
                                               })
                elif "OR" in search_content:
                    content = websites_with_or(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                    return render(request, 'websites.html', {
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
                                                        "filter": "[]" 
                                                        
                                               })
                elif "NOT" in search_content:
                    content = websites_with_not(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                    return render(request, 'websites.html', {
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
                                                        "filter": "[]" 
                                               })
                else :
                    content = websites_with_field(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                    return render(request, 'websites.html', {
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
                                                        "filter": "[]" 
                                               })
            else:
                content = websites_with_content(search_content, page, current_page, last_page, next_page, s_type, index_dict)
                return render(request, 'websites.html', {
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
                                                        "filter": "[]" 
                                               })
        else: #添加过滤条件的搜索
            field_dict = {
                          "全文" : "_all",
                          "网址" : "domain",
                          "国家/地区" : "location.country",
                          "省份" : "location.province",
                          "城市" : "location.city",
                          "updated_at" : "updated_at"
                          }
            field_dict = json.dumps(field_dict)
            field_dict = json.loads(field_dict)
            if ":" in search_content:
                if "AND" in search_content:
                    content = websites_with_and_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
                    return render(request, 'websites.html', {
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
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)         
                                                        
                                               })
                elif "OR" in search_content:
                    content = websites_with_or_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
                    return render(request, 'websites.html', {
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
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)         
                                                        
                                               })
                elif "NOT" in search_content:
                    content = websites_with_not_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
                    return render(request, 'websites.html', {
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
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)         
                                               })
                else :
                    content = websites_with_field_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
                    return render(request, 'websites.html', {
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
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)         
                                               })
            else:
                content = websites_with_content_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict)
                return render(request, 'websites.html', {
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
                                                        "filter": filter,
                                                        "filter_list": json.loads(filter)         
                                               })
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
                                                    "match_phrase": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    },
                                                    {
                                                       "match_phrase":{
                                                           "location.country": "china"
                                                         }
                                                      }
                                                     ]
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        hit_dict["protocols"] = ["9200/http"]
        hit_dict["port"] = "9200"
        hit_dict["protocol"] = "http"
        hit_dict["data"] = hit["_source"]["9200"]["http"]["get"]["body"]
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
                                                    "match_phrase": {
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
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        hit_dict["protocols"] = ["9200/http"]
        hit_dict["port"] = "9200"
        hit_dict["protocol"] = "http"
        hit_dict["data"] = hit["_source"]["9200"]["http"]["get"]["body"]
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
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        highlight = hit.get("highlight",{})
        protocols = []
        if len(highlight.keys()) > 0:
            for key in highlight.keys():
                keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
                if keyreg != None:
                    protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                    if protocol not in protocols:
                        protocols.append(protocol)
            if len(protocols) == 0:
                for protocol in hit["_source"]["protocols"]:
                    protocols.append(protocol)
                hit_dict["protocols"] = protocols
                protocol = hit["_source"]["protocols"][0]
                reg_protocol = re.compile(r'\s*/\s*')
                port = (reg_protocol.split(protocol))[0]
                protocol = (reg_protocol.split(protocol))[1]
                hit_dict["port"] = port
                hit_dict["protocol"] = protocol
                json_data = hit["_source"][port][protocol]
                for key in json_data.keys():
                    hit_dict["data"] = json.dumps(json_data[key], indent=4)
            else:
                hit_dict["protocols"] = protocols
                protocol = protocols[0]
                reg_protocol = re.compile(r'\s*/\s*')
                port = (reg_protocol.split(protocol))[0]
                protocol = (reg_protocol.split(protocol))[1]
                hit_dict["port"] = port
                hit_dict["protocol"] = protocol
                json_data = hit["_source"][port][protocol]
                for key in json_data.keys():
                    hit_dict["data"] = json.dumps(json_data[key], indent=4)
        else:
            hit_dict["protocols"] = protocols
            hit_dict["port"] = ""
            hit_dict["protocol"] = ""
            hit_dict["data"] = "全文检索与字段分词不一致"
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
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                           },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        highlight = hit.get("highlight",{})
        protocols = []
        if len(highlight.keys()) > 0:
            for key in highlight.keys():
                keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
                if keyreg != None:
                    protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                    if protocol not in protocols:
                        protocols.append(protocol)
            if len(protocols) == 0:
                for protocol in hit["_source"]["protocols"]:
                    protocols.append(protocol)
                hit_dict["protocols"] = protocols
                protocol = hit["_source"]["protocols"][0]
                reg_protocol = re.compile(r'\s*/\s*')
                port = (reg_protocol.split(protocol))[0]
                protocol = (reg_protocol.split(protocol))[1]
                hit_dict["port"] = port
                hit_dict["protocol"] = protocol
                json_data = hit["_source"][port][protocol]
                for key in json_data.keys():
                    hit_dict["data"] = json.dumps(json_data[key], indent=4)
            else:
                hit_dict["protocols"] = protocols
                protocol = protocols[0]
                reg_protocol = re.compile(r'\s*/\s*')
                port = (reg_protocol.split(protocol))[0]
                protocol = (reg_protocol.split(protocol))[1]
                hit_dict["port"] = port
                hit_dict["protocol"] = protocol
                json_data = hit["_source"][port][protocol]
                for key in json_data.keys():
                    hit_dict["data"] = json.dumps(json_data[key], indent=4)
        else:
            hit_dict["protocols"] = protocols
            hit_dict["port"] = ""
            hit_dict["protocol"] = ""
            hit_dict["data"] = "全文检索与字段分词不一致"
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
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ]
                                                 }
                                           },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        highlight = hit.get("highlight",{})
        protocols = []
        if len(highlight.keys()) > 0:
            for key in highlight.keys():
                keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
                if keyreg != None:
                    protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                    if protocol not in protocols:
                        protocols.append(protocol)
            if len(protocols) == 0:
                for protocol in hit["_source"]["protocols"]:
                    protocols.append(protocol)
                hit_dict["protocols"] = protocols
                protocol = hit["_source"]["protocols"][0]
                reg_protocol = re.compile(r'\s*/\s*')
                port = (reg_protocol.split(protocol))[0]
                protocol = (reg_protocol.split(protocol))[1]
                hit_dict["port"] = port
                hit_dict["protocol"] = protocol
                json_data = hit["_source"][port][protocol]
                for key in json_data.keys():
                    hit_dict["data"] = json.dumps(json_data[key], indent=4)
            else:
                hit_dict["protocols"] = protocols
                protocol = protocols[0]
                reg_protocol = re.compile(r'\s*/\s*')
                port = (reg_protocol.split(protocol))[0]
                protocol = (reg_protocol.split(protocol))[1]
                hit_dict["port"] = port
                hit_dict["protocol"] = protocol
                json_data = hit["_source"][port][protocol]
                for key in json_data.keys():
                    hit_dict["data"] = json.dumps(json_data[key], indent=4)
        else:
            hit_dict["protocols"] = protocols
            hit_dict["port"] = ""
            hit_dict["protocol"] = ""
            hit_dict["data"] = "全文检索与字段分词不一致"
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
                                        "match_phrase": {
                                            field1: field1_value
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
            
        highlight = hit.get("highlight",{})
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["port"] = port
            hit_dict["protocol"] = protocol
            json_data = hit["_source"][port][protocol]
            for key in json_data.keys():
                hit_dict["data"] = json.dumps(json_data[key], indent=4)
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["port"] = port
            hit_dict["protocol"] = protocol
            json_data = hit["_source"][port][protocol]
            for key in json_data.keys():
                hit_dict["data"] = json.dumps(json_data[key], indent=4)
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
    if search_content != "":
        response = client.search(
                                index=index_dict[s_type],
                                doc_type="ipv4host",
                                body={
                                     "from": (page - 1) * 20,
                                     "size": 20,
                                     "query": {
                                        "match_phrase": {
                                            "_all": search_content
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
                                                }
                                            }
                                      }
                                )
    else:
        response = client.search(
                                index=index_dict[s_type],
                                doc_type="ipv4host",
                                body={
                                     "from": (page - 1) * 20,
                                     "size": 20,
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
                                                }
                                            }
                                      }
                                )
    total_nums = response["hits"]["total"]
    page_nums = int(total_nums / 20) + 1 if (page % 20) > 0 else int(total_nums / 20)
    time_took = float(response["took"]) / 1000
    hit_list = []
    for hit in response["hits"]["hits"]:
        highlight={}
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
        highlight = hit.get("highlight",{})
        protocols = []
        if len(highlight.keys()) > 0:
            for key in highlight.keys():
                keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
                if keyreg != None:
                    protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                    if protocol not in protocols:
                        protocols.append(protocol)
            if len(protocols) == 0:
                for protocol in hit["_source"]["protocols"]:
                    protocols.append(protocol)
                hit_dict["protocols"] = protocols
                protocol = hit["_source"]["protocols"][0]
                reg_protocol = re.compile(r'\s*/\s*')
                port = (reg_protocol.split(protocol))[0]
                protocol = (reg_protocol.split(protocol))[1]
                hit_dict["port"] = port
                hit_dict["protocol"] = protocol
                json_data = hit["_source"][port][protocol]
                for key in json_data.keys():
                    hit_dict["data"] = json.dumps(json_data[key], indent=4)
            else:
                hit_dict["protocols"] = protocols
                protocol = protocols[0]
                reg_protocol = re.compile(r'\s*/\s*')
                port = (reg_protocol.split(protocol))[0]
                protocol = (reg_protocol.split(protocol))[1]
                hit_dict["port"] = port
                hit_dict["protocol"] = protocol
                json_data = hit["_source"][port][protocol]
                for key in json_data.keys():
                    hit_dict["data"] = json.dumps(json_data[key], indent=4)
        else:
            hit_dict["protocols"] = protocols
            hit_dict["port"] = ""
            hit_dict["protocol"] = ""
            hit_dict["data"] = "全文检索与字段分词不一致"
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
def websites_with_and(search_content, page, current_page, last_page, next_page, s_type, index_dict):
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
                                 doc_type="website",
                                 body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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
def websites_with_or(search_content, page, current_page, last_page, next_page, s_type, index_dict):
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
                                doc_type="website",
                                body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "should": [
                                                     {
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                           },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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
def websites_with_not(search_content, page, current_page, last_page, next_page, s_type, index_dict):
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
                                doc_type="website",
                                body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ]
                                                 }
                                           },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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
def websites_with_field(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    reg2 = re.compile(r'\s*:\s*')
    search_list = reg2.split(search_content)
    field1 = search_list[0]
    field1_value = search_list[1]
    response = client.search(
                                 index=index_dict[s_type],
                                 doc_type="website",
                                 body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "match_phrase": {
                                            field1: field1_value
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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
def websites_with_content(search_content, page, current_page, last_page, next_page, s_type, index_dict):
    response = client.search(
                                index=index_dict[s_type],
                                doc_type="website",
                                body={
                                     "from": (page - 1) * 20,
                                     "size": 20,
                                     "query": {
                                        "match_phrase": {
                                            "_all": search_content
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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
def ipv4_es_china_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    protocol_status = 0
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter_field == "protocols":
                protocol_status = 1
                protocol_value = filter[i]["value"]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
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
                                                    "match_phrase": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    },
                                                    {
                                                       "match_phrase":{
                                                           "location.country": "china"
                                                         }
                                                      }
                                                     ],
                                            "filter": filter_query
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        hit_dict["protocols"] = ["9200/http"]
        hit_dict["port"] = "9200"
        hit_dict["protocol"] = "http"
        hit_dict["data"] = hit["_source"]["9200"]["http"]["get"]["body"]
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
def ipv4_es_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
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
                                                    "match_phrase": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    }
                                                     ],
                                            "filter": filter_query
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        hit_dict["protocols"] = ["9200/http"]
        hit_dict["port"] = "9200"
        hit_dict["protocol"] = "http"
        hit_dict["data"] = hit["_source"]["9200"]["http"]["get"]["body"]
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
def ipv4_with_and_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    protocol_status = 0
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter_field == "protocols":
                protocol_status = 1
                protocol_value = filter[i]["value"]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
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
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                             "filter": filter_query
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if protocol_status == 0:
            highlight = hit.get("highlight",{})
            protocols = []
            if len(highlight.keys()) > 0:
                for key in highlight.keys():
                    keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
                    if keyreg != None:
                        protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                        if protocol not in protocols:
                            protocols.append(protocol)
                if len(protocols) == 0:
                    for protocol in hit["_source"]["protocols"]:
                        protocols.append(protocol)
                    hit_dict["protocols"] = protocols
                    protocol = hit["_source"]["protocols"][0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
                else:
                    hit_dict["protocols"] = protocols
                    protocol = protocols[0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
            else:
                hit_dict["protocols"] = protocols
                hit_dict["port"] = ""
                hit_dict["protocol"] = ""
                hit_dict["data"] = "全文检索与字段分词不一致"
        else:
            protocols = []
            protocols.append(protocol_value)
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol_value))[0]
            protocol = (reg_protocol.split(protocol_value))[1]
            hit_dict["protocols"] = protocols
            hit_dict["port"] = port
            hit_dict["protocol"] = protocol
            json_data = hit["_source"][port][protocol]
            for key in json_data.keys():
                hit_dict["data"] = json.dumps(json_data[key], indent=4) 
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
def ipv4_with_or_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    protocol_status = 0
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter_field == "protocols":
                protocol_status = 1
                protocol_value = filter[i]["value"]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
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
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                            "filter": filter_query
                                                 }
                                           },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if protocol_status == 0:
            highlight = hit.get("highlight",{})
            protocols = []
            if len(highlight.keys()) > 0:
                for key in highlight.keys():
                    keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
                    if keyreg != None:
                        protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                        if protocol not in protocols:
                            protocols.append(protocol)
                if len(protocols) == 0:
                    for protocol in hit["_source"]["protocols"]:
                        protocols.append(protocol)
                    hit_dict["protocols"] = protocols
                    protocol = hit["_source"]["protocols"][0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
                else:
                    hit_dict["protocols"] = protocols
                    protocol = protocols[0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
            else:
                hit_dict["protocols"] = protocols
                hit_dict["port"] = ""
                hit_dict["protocol"] = ""
                hit_dict["data"] = "全文检索与字段分词不一致"
        else:
            protocols = []
            protocols.append(protocol_value)
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol_value))[0]
            protocol = (reg_protocol.split(protocol_value))[1]
            hit_dict["protocols"] = protocols
            hit_dict["port"] = port
            hit_dict["protocol"] = protocol
            json_data = hit["_source"][port][protocol]
            for key in json_data.keys():
                hit_dict["data"] = json.dumps(json_data[key], indent=4) 
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
def ipv4_with_not_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    protocol_status = 0
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter_field == "protocols":
                protocol_status = 1
                protocol_value = filter[i]["value"]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
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
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ],
                                            "filter": filter_query
                                                 }
                                           },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if protocol_status == 0:
            highlight = hit.get("highlight",{})
            protocols = []
            if len(highlight.keys()) > 0:
                for key in highlight.keys():
                    keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
                    if keyreg != None:
                        protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                        if protocol not in protocols:
                            protocols.append(protocol)
                if len(protocols) == 0:
                    for protocol in hit["_source"]["protocols"]:
                        protocols.append(protocol)
                    hit_dict["protocols"] = protocols
                    protocol = hit["_source"]["protocols"][0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
                else:
                    hit_dict["protocols"] = protocols
                    protocol = protocols[0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
            else:
                hit_dict["protocols"] = protocols
                hit_dict["port"] = ""
                hit_dict["protocol"] = ""
                hit_dict["data"] = "全文检索与字段分词不一致"
        else:
            protocols = []
            protocols.append(protocol_value)
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol_value))[0]
            protocol = (reg_protocol.split(protocol_value))[1]
            hit_dict["protocols"] = protocols
            hit_dict["port"] = port
            hit_dict["protocol"] = protocol
            json_data = hit["_source"][port][protocol]
            for key in json_data.keys():
                hit_dict["data"] = json.dumps(json_data[key], indent=4) 
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
def ipv4_with_field_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    protocol_status = 0
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter_field == "protocols":
                protocol_status = 1
                protocol_value = filter[i]["value"]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
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
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "filter": filter_query
                                                }
                                            },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if protocol_status == 0:
            highlight = hit.get("highlight",{})
            protocols = []
            if len(highlight.keys()) > 0:
                for key in highlight.keys():
                    keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
                    if keyreg != None:
                        protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                        if protocol not in protocols:
                            protocols.append(protocol)
                if len(protocols) == 0:
                    for protocol in hit["_source"]["protocols"]:
                        protocols.append(protocol)
                    hit_dict["protocols"] = protocols
                    protocol = hit["_source"]["protocols"][0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
                else:
                    hit_dict["protocols"] = protocols
                    protocol = protocols[0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
            else:
                hit_dict["protocols"] = protocols
                hit_dict["port"] = ""
                hit_dict["protocol"] = ""
                hit_dict["data"] = "全文检索与字段分词不一致"
        else:
            protocols = []
            protocols.append(protocol_value)
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol_value))[0]
            protocol = (reg_protocol.split(protocol_value))[1]
            hit_dict["protocols"] = protocols
            hit_dict["port"] = port
            hit_dict["protocol"] = protocol
            json_data = hit["_source"][port][protocol]
            for key in json_data.keys():
                hit_dict["data"] = json.dumps(json_data[key], indent=4) 
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
def ipv4_with_content_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    protocol_status = 0
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter_field == "protocols":
                protocol_status = 1
                protocol_value = filter[i]["value"]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
    if search_content != "":
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
                                                      "match_phrase":{
                                                               "_all" : search_content
                                                               }
                                                      }
                                                     ],
                                            "filter": filter_query
                                                }
                                            },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
                                                }
                                            }
                                      }
                                )
    else:
        response = client.search(
                                index=index_dict[s_type],
                                doc_type="ipv4host",
                                body={
                                     "from": (page - 1) * 20,
                                     "size": 20,
                                     "query": {
                                        "bool": {
                                            "filter": filter_query
                                                }
                                            },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if protocol_status == 0:
            highlight = hit.get("highlight",{})
            protocols = []
            if len(highlight.keys()) > 0:
                for key in highlight.keys():
                    keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
                    if keyreg != None:
                        protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                        if protocol not in protocols:
                            protocols.append(protocol)
                if len(protocols) == 0:
                    for protocol in hit["_source"]["protocols"]:
                        protocols.append(protocol)
                    hit_dict["protocols"] = protocols
                    protocol = hit["_source"]["protocols"][0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
                else:
                    hit_dict["protocols"] = protocols
                    protocol = protocols[0]
                    reg_protocol = re.compile(r'\s*/\s*')
                    port = (reg_protocol.split(protocol))[0]
                    protocol = (reg_protocol.split(protocol))[1]
                    hit_dict["port"] = port
                    hit_dict["protocol"] = protocol
                    json_data = hit["_source"][port][protocol]
                    for key in json_data.keys():
                        hit_dict["data"] = json.dumps(json_data[key], indent=4)
            else:
                hit_dict["protocols"] = protocols
                hit_dict["port"] = ""
                hit_dict["protocol"] = ""
                hit_dict["data"] = "全文检索与字段分词不一致"
        else:
            protocols = []
            protocols.append(protocol_value)
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol_value))[0]
            protocol = (reg_protocol.split(protocol_value))[1]
            hit_dict["protocols"] = protocols
            hit_dict["port"] = port
            hit_dict["protocol"] = protocol
            json_data = hit["_source"][port][protocol]
            for key in json_data.keys():
                hit_dict["data"] = json.dumps(json_data[key], indent=4) 
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

def websites_with_and_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
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
                                 doc_type="website",
                                 body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                             "filter": filter_query
                                                 }
                                         },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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
def websites_with_or_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
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
                                doc_type="website",
                                body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "should": [
                                                     {
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                            "filter": filter_query
                                                 }
                                           },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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
def websites_with_not_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
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
                                doc_type="website",
                                body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match_phrase":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ],
                                            "filter": filter_query
                                                 }
                                           },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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
def websites_with_field_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
    reg2 = re.compile(r'\s*:\s*')
    search_list = reg2.split(search_content)
    field1 = search_list[0]
    field1_value = search_list[1]
    response = client.search(
                                 index=index_dict[s_type],
                                 doc_type="website",
                                 body={
                                   "from": (page - 1) * 20,
                                   "size": 20,
                                   "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match_phrase":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "filter": filter_query
                                                }
                                            },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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
def websites_with_content_with_filter(search_content, page, current_page, last_page, next_page, s_type, index_dict, filter, field_dict):
    code = str(type(filter))
    if code == "<type 'unicode'>":
        filter = filter.encode("utf-8") 
        filter = json.loads(filter)
    else:
        filter = json.loads(filter)
    filter_query = []
    for i in range(len(filter)):
        if filter[i] != "":
            filter_field = field_dict[filter[i]["field"]]
            if filter[i]["way"] == "filter":
                if filter[i]["field_way"] == "equal":
                    filter_dict = {}
                    filter_dict["match_phrase"] = {
                                                   filter_field : filter[i]["value"]
                                                   }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "not_equal":
                    filter_dict = {}
                    filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                    filter_query.append(filter_dict)
                elif filter[i]["field_way"] == "in":
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["match_phrase"] = {
                                                       filter_field : filter[i]["value"][j]
                                                       }
                        filter_query.append(filter_dict)
                else:
                    for j in range(len(filter[i]["value"])):
                        filter_dict = {}
                        filter_dict["bool"] = {
                                           "must_not":{
                                                 "match_phrase":{
                                                         filter_field : filter[i]["value"]     
                                                                 }  
                                                   }
                                           }
                        filter_query.append(filter_dict)
            elif filter[i]["way"] == "range":
                if filter[i]["field_way"] == "in":
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "lte" : to_value       
                                                             }
                                              }
                    elif to_value == "":
                        filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value       
                                                             }
                                              }
                    filter_dict["range"] = {
                                              filter_field :{
                                                      "gte" : from_value ,
                                                      "lte" : to_value 
                                                             }
                                              }
                    filter_query.append(filter_dict)
                else:
                    filter_dict = {}
                    from_value = filter[i]["value"][0]
                    to_value = filter[i]["value"][1]
                    if from_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "lte" : to_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    elif to_value == "":
                        filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value        
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_dict["bool"] = {
                                              "must_not":{
                                                     "range":{
                                                         filter_field:{
                                                                 "gte" : from_value ,
                                                                 "lte" : to_value 
                                                                       }     
                                                              }     
                                                          }
                                              }
                    filter_query.append(filter_dict)
    response = client.search(
                                index=index_dict[s_type],
                                doc_type="website",
                                body={
                                     "from": (page - 1) * 20,
                                     "size": 20,
                                     "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match_phrase":{
                                                               "_all" : search_content
                                                               }
                                                      }
                                                     ],
                                            "filter": filter_query
                                                }
                                            },
                                     "highlight": {
                                         "require_field_match": "false",
                                         "fields": {
                                              "*": {}
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
        if hit["_source"].has_key("domain") == True:
            hit_dict["domain"] = hit["_source"]["domain"]
        else:
            hit_dict["domain"] = ""
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
        highlight = hit["highlight"]
        protocols = []
        for key in highlight.keys():
            keyreg = re.match('(?P<port>\d+)\.(?P<protocol>[^\.]+)',key)
            if keyreg != None:
                protocol = keyreg.group('port')+"/"+keyreg.group('protocol')
                if protocol not in protocols:
                    protocols.append(protocol)
        if len(protocols) == 0:
            for protocol in hit["_source"]["protocols"]:
                protocols.append(protocol)
            hit_dict["protocols"] = protocols
            protocol = hit["_source"]["protocols"][0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
        else:
            hit_dict["protocols"] = protocols
            protocol = protocols[0]
            reg_protocol = re.compile(r'\s*/\s*')
            port = (reg_protocol.split(protocol))[0]
            protocol = (reg_protocol.split(protocol))[1]
            hit_dict["headers"] = json.dumps(hit["_source"][port][protocol]["get"]["headers"],indent=4)
            if hit["_source"][port][protocol]["get"].has_key("metadata") == True:
                hit_dict["metadata"] = json.dumps(hit["_source"][port][protocol]["get"]["metadata"],indent=4)
            else :
                hit_dict["metadata"] = ""
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




    
