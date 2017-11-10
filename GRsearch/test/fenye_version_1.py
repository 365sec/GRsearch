# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
from elasticsearch import Elasticsearch

client = Elasticsearch("172.16.39.233:9200")

def search(request):
    search_content = request.GET.get('q', '')   
    page = int(request.GET.get("page", "1"))
    s_type = request.GET.get("s_type", "webscan")
    index_dict = {
                  "webscan": "scan",
                  "portscan": "portscan-2017.08.21"
                  }
    
    response = client.search(
                             index=index_dict[s_type],
                             doc_type="t_engin_task_detail",
                             body={
                                   "from": (page - 1)* 20,
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
    page_list = [
            i for i in range(page-4, page+5) if 0 < i <= page_nums      # 分页页码列表
        ]
    return render(request, 'fenye.html',{"all_hits":hit_list, "search_content": search_content, "total_nums":total_nums, "time_took":time_took, "page_nums":page_nums,"page_list":page_list,"s_type":s_type })
