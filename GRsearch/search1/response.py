# -*- coding: utf-8 -*-

from django.shortcuts import render
from elasticsearch import Elasticsearch
import urllib2
import json


def response(request):
    context = {}
    es = Elasticsearch("172.16.39.233:9200")
    index = "scan"
    type = "t_engin_server_his"
    map = es.indices.get_mapping(index, doc_type=type)
    mapping = map[index]["mappings"][type]["properties"]
    query = {
             "size": 100,
             "query":{
                      "match_all":{}
                      }
             }
    res = es.search(index, type,body=query)
    index = res["hits"]["hits"][0]["_index"]
    type = res["hits"]["hits"][0]["_type"]
    doc_count = res["hits"]["total"]
    doc = res["hits"]["hits"][0]
    hits = res["hits"]["hits"]
    context['index']=index
    context['type']=type
    context['mapping']= json.dumps(mapping)
    context['doc']= json.dumps(doc)
    context['doc_count']=doc_count
    context['hits']=json.dumps(hits)
    return render(request, 'response.html', context)

# def url_response(request):
#     #通过rest接口进行查询
#     context = {}
#     index = "webscan"
#     url = "http://172.16.39.160:9305/"+index+"/_search"
#     query = {
#              "query":{
#                       "match_all":{}
#                       }
#              }
#     query = json.dumps(query)
#     req = urllib2.Request(url,query)
#     result = urllib2.urlopen(req)
#     res = result.read()
#     res = json.loads(res)
#     context['index']= "webscan1"
#     index = res["hits"]["hits"][0]["_index"]
#     type = res["hits"]["hits"][0]["_type"] 
#     context['index']=index
#     context['type']=type
#     doc = res["hits"]["hits"][0]
#     context['doc']=json.dumps(doc,indent=2)##
#     return render(request, 'response.html', context)
#         
# def response_1(request):
#     context = {}
#     es = Elasticsearch("172.16.39.160:9305")
#     index = "webscan"
#     type = "t_engin_task_detail_edit"
#     query = {
#              "query":{
#                       "match_all":{}
#                       }
#              }
#     res = es.search(index, type,body=query)
#     index = res["hits"]["hits"][0]["_index"]
#     type = res["hits"]["hits"][0]["_type"]
#     doc_count = res["hits"]["total"]
#     doc = res["hits"]["hits"][0]
#     source = res["hits"]["hits"][0]["_source"]
#     dl_content = ""
#     for key in source:
#         value = source[key]
#         dl = "<dt>"+key+":</dt><dd>"+str(value)+"</dd>"
#         dl_content = dl_content+dl
#     
#     context['index']=index
#     context['type']=type
#     context['doc']= json.dumps(doc)
#     context['doc_count']=doc_count
#     context['dl_content']=json.dumps(dl_content)
#     return render(request, 'response.html', context)
# 
# def response_2(request):
#     context = {}
#     es = Elasticsearch("172.16.39.160:9305")
#     index = "webscan"
#     type = "t_engin_server_his"
#     query = {
#              "query":{
#                       "match_all":{}
#                       }
#              }
#     res = es.search(index, type,body=query)
#     index = res["hits"]["hits"][0]["_index"]
#     type = res["hits"]["hits"][0]["_type"]
#     doc_count = res["hits"]["total"]
#     doc = res["hits"]["hits"][0]
#     source = res["hits"]["hits"][0]["_source"]
#     context['index']=index
#     context['type']=type
#     context['doc']= json.dumps(doc)
#     context['doc_count']=doc_count
#     context['dl_content']=json.dumps(source)
#     return render(request, 'response.html', context)