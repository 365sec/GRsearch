# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
from elasticsearch import Elasticsearch

client = Elasticsearch("172.16.39.233:9200")

def search(request):
    _id = request.GET.get('q', '')
    response = client.get(index="portscan-2017.08.21", id=_id, doc_type="test")
    source = response["_source"]  #这里对于是否存在没有多加判断
    es_port_list = []  #端口列表
    es_port_filed_list = [] #端口字段列表
    protocols = []  #端口对应的协议列表
    for k in source.keys():
        reg1 = re.search(r'(?<=p)\d+',k)
        if reg1:
            es_port_list.append(reg1.group(0))
            es_port_filed_list.append(k)
            list1 = []
            for k1 in response["_source"][k].keys():
                list1.append(k1)
            protocols.append(list1[0])
        else:
            print ""
    
    metainfo = {}
    metainfo["ip"] = response["_source"]["ip"]
    metainfo["country"] = response["_source"]["location"]["country"]
    metainfo["province"] = response["_source"]["location"]["province"]
    metainfo["city"] = response["_source"]["location"]["city"]
    metainfo["longitude"] = response["_source"]["location"]["longitude"]
    metainfo["latitude"] = response["_source"]["location"]["latitude"]
    port_list = []
    port_name_list = []
    for i in range(len(es_port_list)):
        port_dict = {}
        port_dict["port"] = es_port_list[i]        
        port_dict["protocol"] = protocols[i]
        if port_dict["protocol"]=="http":
            port_dict["headers"] = json.dumps(response["_source"][es_port_filed_list[i]]["http"]["get"]["headers"],indent=4)
            if response["_source"][es_port_filed_list[i]]["http"]["get"].has_key("body") == True:
                port_dict["body"] = response["_source"][es_port_filed_list[i]]["http"]["get"]["body"]
            else :
                port_dict["body"] = ""
        elif port_dict["protocol"]=="https":
            if response["_source"][es_port_filed_list[i]]["https"].has_key("tls") == True:
                port_dict["tls"] = json.dumps(response["_source"][es_port_filed_list[i]]["https"]["tls"],indent=4)
            else :
                port_dict["tls"] = ""
        elif port_dict["protocol"]=="ssh":
            if response["_source"][es_port_filed_list[i]]["ssh"].has_key("banner") == True:
                port_dict["banner_data"] = json.dumps(response["_source"][es_port_filed_list[i]]["ssh"]["banner"],indent=4)
            else:
                port_dict["banner_data"] = ""
        elif port_dict["protocol"]=="ftp":
            if response["_source"][es_port_filed_list[i]]["ftp"].has_key("banner") == True:
                port_dict["banner_data"] = json.dumps(response["_source"][es_port_filed_list[i]]["ftp"]["banner"],indent=4)
            else:
                port_dict["banner_data"] = ""
        #以下直接展示data数据
#         elif port_dict["protocol"]=="mysql":
#             port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["mysql"])
# #             if response["_source"][es_port_filed_list[i]]["mysql"].has_key("banner") == True:
# #                 port_dict["banner_data"] = json.dumps(response["_source"][es_port_filed_list[i]]["mysql"]["banner"])
# #             else:
# #                 port_dict["banner_data"] = ""
#         elif port_dict["protocol"]=="pop3":
#             port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["pop3"])
# #             if response["_source"][es_port_filed_list[i]]["pop3"].has_key("starttls") == True:
# #                 port_dict["starttls"] = json.dumps(response["_source"][es_port_filed_list[i]]["pop3"]["starttls"])
# #             else:
# #                 port_dict["starttls"] = ""
#         elif port_dict["protocol"]=="pop3s":
#             port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["pop3s"])
# #             if response["_source"][es_port_filed_list[i]]["pop3s"].has_key("tls") == True:
# #                 port_dict["tls"] = json.dumps(response["_source"][es_port_filed_list[i]]["pop3s"]["tls"])
# #             else:
# #                 port_dict["tls"] = ""
#         elif port_dict["protocol"]=="imaps":
#             port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["imaps"])
# #             if response["_source"][es_port_filed_list[i]]["imaps"].has_key("tls") == True:
# #                 port_dict["tls"] = json.dumps(response["_source"][es_port_filed_list[i]]["imaps"]["tls"])
# #             else:
# #                 port_dict["tls"] = ""
#         elif port_dict["protocol"]=="smtps":
#             port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["smtps"])
# #             if response["_source"][es_port_filed_list[i]]["smtps"].has_key("ssl_2") == True:
# #                 port_dict["ssl_2"] = json.dumps(response["_source"][es_port_filed_list[i]]["smtps"]["ssl_2"])
# #             else:
# #                 port_dict["ssl_2"] = ""
#         elif port_dict["protocol"]=="cwmp":
#             if response["_source"][es_port_filed_list[i]].has_key("cwmp") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["cwmp"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="telnet":
#             if response["_source"][es_port_filed_list[i]].has_key("telnet") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["telnet"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="known-private-key":
#             if response["_source"][es_port_filed_list[i]].has_key("known-private-key") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["known-private-key"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="rsa-export":
#             if response["_source"][es_port_filed_list[i]].has_key("rsa-export") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["rsa-export"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="smb":
#             if response["_source"][es_port_filed_list[i]].has_key("smb") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["smb"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="dhe-export":
#             if response["_source"][es_port_filed_list[i]].has_key("dhe-export") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["dhe-export"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="Update utility":
#             if response["_source"][es_port_filed_list[i]].has_key("Update utility") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["Update utility"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="heartbleed":
#             if response["_source"][es_port_filed_list[i]].has_key("heartbleed") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["heartbleed"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="embedded":
#             if response["_source"][es_port_filed_list[i]].has_key("embedded") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["embedded"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="building control":
#             if response["_source"][es_port_filed_list[i]].has_key("building control") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["building control"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="scada":
#             if response["_source"][es_port_filed_list[i]].has_key("scada") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["scada"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="fox":
#             if response["_source"][es_port_filed_list[i]].has_key("fox") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["fox"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="modbus":
#             if response["_source"][es_port_filed_list[i]].has_key("modbus") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["modbus"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="NPM":
#             if response["_source"][es_port_filed_list[i]].has_key("NPM") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["NPM"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="bacnet":
#             if response["_source"][es_port_filed_list[i]].has_key("bacnet") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["bacnet"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="strip-starttls":
#             if response["_source"][es_port_filed_list[i]].has_key("strip-starttls") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["strip-starttls"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="NPM6":
#             if response["_source"][es_port_filed_list[i]].has_key("NPM6") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["NPM6"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="remote access":
#             if response["_source"][es_port_filed_list[i]].has_key("remote access") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["remote access"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="s7":
#             if response["_source"][es_port_filed_list[i]].has_key("s7") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["s7"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="NPM2":
#             if response["_source"][es_port_filed_list[i]].has_key("NPM2") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["NPM2"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="NPM3":
#             if response["_source"][es_port_filed_list[i]].has_key("NPM3") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["NPM3"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="JACE":
#             if response["_source"][es_port_filed_list[i]].has_key("JACE") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["JACE"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="Running DD-WRT":
#             if response["_source"][es_port_filed_list[i]].has_key("Running DD-WRT") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["Running DD-WRT"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="JACE-7":
#             if response["_source"][es_port_filed_list[i]].has_key("JACE-7") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["JACE-7"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="Broken installation":
#             if response["_source"][es_port_filed_list[i]].has_key("Broken installation") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["Broken installation"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="JACE-403":
#             if response["_source"][es_port_filed_list[i]].has_key("JACE-403") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["JACE-403"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="JACE-545":
#             if response["_source"][es_port_filed_list[i]].has_key("JACE-545") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["JACE-545"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="dnp3":
#             if response["_source"][es_port_filed_list[i]].has_key("dnp3") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["dnp3"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="touchscreen":
#             if response["_source"][es_port_filed_list[i]].has_key("touchscreen") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["touchscreen"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="ethernet":
#             if response["_source"][es_port_filed_list[i]].has_key("ethernet") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["ethernet"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="scada processor":
#             if response["_source"][es_port_filed_list[i]].has_key("scada processor") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["scada processor"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="JACE-402":
#             if response["_source"][es_port_filed_list[i]].has_key("JACE-402") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["JACE-402"])
#             else :
#                 port_dict["data"] = ""
#         elif port_dict["protocol"]=="data center":
#             if response["_source"][es_port_filed_list[i]].has_key("data center") == True:
#                 port_dict["data"] =json.dumps(response["_source"][es_port_filed_list[i]]["data center"])
#             else :
#                 port_dict["data"] = ""
        else :
            port_dict["data"] = json.dumps(response["_source"][es_port_filed_list[i]],indent=4)
        port_name_list.append(es_port_list[i])
        port_list.append(port_dict)
    return render(request,'portscan_detail.html',{
                                       "port_name_list": port_name_list,
                                       "port_list": port_list,
                                       "metainfo": metainfo
                                       })
    
        