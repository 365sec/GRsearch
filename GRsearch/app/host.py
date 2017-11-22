# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
import urllib2
from elasticsearch import Elasticsearch

client = Elasticsearch("172.16.39.233:9200")

def search(request):
    _id = request.GET.get('q', '')
    response = client.get(index="ipv4", id=_id, doc_type="ipv4host")
    protocols = response["_source"]["protocols"]  #这里对于是否存在没有多加判断
    metainfo = {}
    metainfo["ip"] = response["_source"]["ip"]
    metainfo["update_time"] = response["_source"]["updated_at"]
    metainfo["country"] = response["_source"]["location"]["country"]
    metainfo["province"] = response["_source"]["location"]["province"]
    metainfo["city"] = response["_source"]["location"]["city"]
    metainfo["longitude"] = response["_source"]["location"]["longitude"]
    metainfo["latitude"] = response["_source"]["location"]["latitude"]
    port_list = []
    port_name_list = []
    for protocol in protocols:
        port_dict = {}
        port_dict["port"] = protocol.split('/')[0]
        port_dict["protocol"] = protocol.split('/')[1]
        if port_dict["protocol"]=="http":
            port_dict["headers"] = json.dumps(response["_source"][protocol.split('/')[0]]["http"]["get"]["headers"],indent=4)
            if response["_source"][protocol.split('/')[0]]["http"]["get"].has_key("body") == True:
                port_dict["body"] = response["_source"][protocol.split('/')[0]]["http"]["get"]["body"]
            else :
                port_dict["body"] = ""
            if port_dict["port"]=="9200":
                reg1 = r'\"number\"\s*:\s*\"[1256]'
                m = re.search(reg1,port_dict["body"])
                if m != None:
                  port_dict["cat_status"] = "yes"
                  try:
                    nodes_status_url = "http://"+metainfo["ip"]+":9200/_cat/nodes/?v&h=ip,disk.avail,heap.max,ram.max"
                    response1 = urllib2.urlopen(nodes_status_url)
                    content1 = response1.read()
                    a = re.split('[\n]',content1)
                    i = 1
                    list1 = []
                    list2 = []
                    list3 = []
                    num_of_nodes = len(a)-2
                    while i < (len(a)-1):
                        res1 = re.search(r'\d*\.\d*\.\d*\.\d*\s*(?P<name1>[^\s]*)\s*(?P<name2>[^\s]*)\s*(?P<name3>[^\s]*)',a[i])
                        list1.append(res1.group("name1"))
                        list2.append(res1.group("name2"))
                        list3.append(res1.group("name3"))
                        i += 1
                    j = 0
                    disk_available_all = 0
                    while j<len(list1):
                        res2 = re.search(r'(?P<num>[^tgmb]*)(?P<boost>.+)',list1[j])
                        if res2.group("boost") == "tb":
                            disk_available = float(res2.group("num"))*1024
                            disk_available_all += disk_available
                        elif res2.group("boost") == "gb":
                            disk_available = float(res2.group("num"))
                            disk_available_all += disk_available
                        elif res2.group("boost") == "mb":
                            disk_available = float(res2.group("num"))/1024
                            disk_available_all += disk_available
                        elif res2.group("boost") == "b":
                            disk_available = float(res2.group("num"))/1024/1024
                            disk_available_all += disk_available
                        j +=1
                    if disk_available_all > 1024:
                        disk_available_all = disk_available_all/1024
                        disk_available_all = str(disk_available_all)+"tb"
                    elif disk_available_all > 1:
                        disk_available_all = str(disk_available_all)+"gb"
                    else:
                        disk_available_all = disk_available_all/1024/1024
                        disk_available_all = str(disk_available_all)+"mb"
                    port_dict["num_of_nodes"] = num_of_nodes
                    port_dict["disk_available_all"] = disk_available_all
                    port_dict["nodes_info"] = content1
                    url = "http://"+metainfo["ip"]+":9200/_cat/indices?v&h=index,docs.count,store.size"
                    response = urllib2.urlopen(url)
                    content2 = response.read()
                    a = re.split('[\n]',content2)
                    i = 1
                    list1 = []
                    list2 = []
                    while i < (len(a)-1):
                        res1 = re.search(r'[^\s]*\s*(?P<name1>[^\s]*)\s*(?P<name2>[^\s]*)',a[i])
                        list1.append(res1.group("name1"))
                        list2.append(res1.group("name2"))
                        i += 1
                    j = 0
                    index_size_all = 0
                    while j<len(list2):
                        res2 = re.search(r'(?P<num>[^tgmkb]*)(?P<boost>.+)',list2[j])
                        if res2.group("boost") == "tb":
                            index_size = float(res2.group("num"))*1024
                            index_size_all += index_size
                        elif res2.group("boost") == "gb":
                            index_size = float(res2.group("num"))
                            index_size_all += index_size
                        elif res2.group("boost") == "mb":
                           index_size = float(res2.group("num"))/1024
                           index_size_all += index_size
                        elif res2.group("boost") == "kb":
                            index_size = float(res2.group("num"))/1024/1024
                            index_size_all += index_size
                        elif res2.group("boost") == "b":
                            index_size = float(res2.group("num"))/1024/1024/1024
                            index_size_all += index_size
                        j +=1
#                     aa = index_size_all   #测试用
                    if index_size_all > 1024:
                        index_size_all = round(index_size_all/1024,2)
                        index_size_all = str(index_size_all)+"tb"
                    elif index_size_all > 1:
                        index_size_all = round(index_size_all,2)
                        index_size_all = str(index_size_all)+"gb"
                    elif index_size_all > 0.0009765625:
                        index_size_all = round(index_size_all*1024,2)
                        index_size_all = str(index_size_all)+"mb"
                    else :
                        index_size_all = round(index_size_all*1024*1024,2)
                        index_size_all = str(index_size_all)+"kb"
                    port_dict["index_info"] = content2
                    port_dict["index_size_all"] = index_size_all
                    port_dict["read_status"] = "success"
#                     port_dict["aa"] = aa
                  except:
                      port_dict["read_status"] = "fail"
                else:
                    port_dict["cat_status"] = "no"
        elif port_dict["protocol"]=="mysql":
            if response["_source"][protocol.split('/')[0]]["mysql"]["banner"].has_key("data") == True:
                port_dict["banner_data"] = json.dumps(response["_source"][protocol.split('/')[0]]["mysql"]["banner"]["data"],indent=4)
            else :
                port_dict["banner_data"] = ""
            if response["_source"][protocol.split('/')[0]]["mysql"]["banner"].has_key("metadata") == True:
                port_dict["metadata"] = json.dumps(response["_source"][protocol.split('/')[0]]["mysql"]["banner"]["metadata"],indent=4)
            else :
                port_dict["metadata"] = ""
        else:
            if response["_source"][port_dict["port"]][port_dict["protocol"]]["banner"].has_key("metadata") == True:
                port_dict["metadata"] = json.dumps(response["_source"][port_dict["port"]][port_dict["protocol"]]["banner"]["metadata"],indent=4)
            else :
                port_dict["metadata"] = ""
            port_dict["banner_data"] = json.dumps(response["_source"][protocol.split('/')[0]],indent=4)
        port_name_list.append(protocol.split('/')[0])
        port_list.append(port_dict)
    return render(request,'host.html',{
                                       "port_name_list": port_name_list,
                                       "port_list": port_list,
                                       "metainfo": metainfo
                                       })
    
        