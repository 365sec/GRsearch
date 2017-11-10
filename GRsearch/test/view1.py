# -*- coding:utf-8 -*-

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
    total_nums = response["hits"]["total"]
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        if "result" in hit["highlight"]:
            hit_dict["result"] = "".join(hit["highlight"]["result"])
        else:
            hit_dict["result"] = hit["_source"]["result"]
        hit_dict["site"] = hit["_source"]["site_url"]
        print hit_dict["result"]
        hit_list.append(hit_dict)
    print str(hit_list)
    
if __name__ == "__main__":
    search()
