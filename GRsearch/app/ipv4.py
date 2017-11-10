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
                  "portscan": "ipv4"
                  }
    if s_type == "webscan":
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
        return render(request, 'fenye_ipv4.html', {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": page,
                                             "page_list":page_list,
                                             "s_type":s_type })
    else:
        es_list = ["es","elasticsearch","9200"]
        if search_content in es_list:
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
                                                     "match": {
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
                hit_dict["ip"] = hit["_source"]["ip"]
                hit_dict["country"] = hit["_source"]["location"]["country"]
                hit_dict["province"] = hit["_source"]["location"]["province"]
                hit_dict["city"] = hit["_source"]["location"]["city"]
                hit_dict["update_time"] = hit["_source"]["updated_at"]
                hit_list.append(hit_dict)
            page_list = [
                         i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
                         ]
            aggs = client.search(
                             index=index_dict[s_type],
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
                                                     "match": {
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
                                         },
                                     "aggs": {
                                          "country": {
                                             "terms": {
                                                "field": "location.country.keyword",
                                                "size": 10
                                                  }
                                               },
                                         "province":{
                                              "terms": {
                                                 "field": "location.country.keyword",
                                                 "size": 10
                                                    }
                                                },
                                         "city":{
                                             "terms": {
                                                 "field": "location.city.keyword",
                                                 "size": 10
                                                }
                                            }
                                          }
                                }
                             )
        response = client.search(
                             index=index_dict[s_type],
                             doc_type="ipv4host",
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
            hit_dict["ip"] = hit["_source"]["ip"]
            hit_dict["country"] = hit["_source"]["location"]["country"]
            hit_dict["city"] = hit["_source"]["location"]["city"]
            hit_dict["tags"] = hit["_source"]["tags"][0]
            hit_list.append(hit_dict)
        page_list = [
                i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
            ]
        while page == 1:
            agg1 = client.search(
                             index=index_dict[s_type],
                             doc_type="test",
                             body={
                                     "size": 0,
                                     "query": {
                                        "match_phrase": {
                                              "_all": "xss"
                                                   }
                                               },
                                     "aggs": {
                                          "service": {
                                             "terms": {
                                                "field": "tags.keyword",
                                                "size": 10
                                                  }
                                               }
                                          }
                                }
                             )
            service_list = []
            for bucket in agg1["aggregations"]["service"]["buckets"]:  #聚合中每个桶的内容
                agg1_dict = {}
                agg1_dict["service_name"] = bucket["key"]
                agg1_dict["count"] = bucket["doc_count"]
                service_list.append(agg1_dict)
        return render(request, 'portscan.html', {
                                             "all_hits":hit_list,
                                             "search_content": search_content,
                                             "total_nums":total_nums,
                                             "time_took":time_took,
                                             "page_nums":page_nums,
                                             "current_page": page,
                                             "page_list":page_list,
                                             "s_type":s_type,
                                             "service_list":service_list
                                              })
    
