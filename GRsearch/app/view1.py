# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
from elasticsearch import Elasticsearch

client = Elasticsearch("172.16.39.233:9200")

def search(request):
    search_content = request.GET.get('q', '')   
    response = client.search(
                             index="scan",
                             doc_type="t_engin_task_detail",
                             body={
                                   "size": 100,
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
    time_took = float(response["took"])/1000
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
    return render(request, 'result.html',{"all_hits":hit_list, "search_content": search_content, "total_nums":total_nums, "time_took":time_took})
