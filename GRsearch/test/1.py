# -*-coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
from elasticsearch import Elasticsearch

client = Elasticsearch("172.16.39.233:9200")

def search():
    search_content = "攻击"
    response = client.search(
                             index="scan",
                             doc_type="t_engin_task_detail",
                             body={
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
    for hit in response["hits"]["hits"]:
        print hit["_source"]["result"]
    
if __name__ == "__main__":
    search()
