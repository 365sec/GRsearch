# -*- coding:utf-8 -*-

import json
import re
import urllib2
from elasticsearch import Elasticsearch



url = "http://180.97.185.130:9200/_cat/indices?v&h=index,docs.count,store.size"
response = urllib2.urlopen(url)
content2 = response.read()
print content2.split('\n')[0]
a = re.split('[\n]',content2)
print a
i = 1
list1 = []
list2 = []
list3 = []
while i < (len(a)-1):
    res1 = re.search(r'[^\s]*\s*(?P<name1>[^\s]*)\s*(?P<name2>[^\s]*)',a[i])
    list1.append(res1.group("name1"))
    list2.append(res1.group("name2"))
    i += 1
j = 0
print list1
print list2
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
if index_size_all > 1024:
    index_size_all = round(index_size_all/1024,2)
    index_size_all = str(disk_available_all)+"tb"
elif index_size_all > 1:
    index_size_all = round(index_size_all,2)
    index_size_all = str(disk_available_all)+"gb"
elif index_size_all > 0.0009765625:
    index_size_all = round(index_size_all/1024/1024,2)
    index_size_all = str(disk_available_all)+"mb"
else :
    index_size_all = round(index_size_all/1024/1024,2)
    index_size_all = str(disk_available_all)+"kb"























# a = r'number\s*a'
# b = "abcbnumber a"
# m = re.match(a,b)
# print m




















# 
# def a(b,c,d,e,f,g,h,i):
#     return b+c+d+e+f+g+h+i 
#     
# if __name__ == '__main__':
#     x = a(1,2,3,4,5,6,7,8)
#     print x














# client = Elasticsearch("172.16.39.233:9200")
# response = client.get(index="ipv4", id="988840764", doc_type="ipv4host")
# if response["_source"]["9200"]["http"]["get"].has_key("body") == True:
#     print response["_source"][protocol.split('/')[0]]["http"]["get"]["body"]
# else: 
#     print "ok"




# a = "a:b   AND   c:d"
# if "AND" in a:
#     p = re.compile(r'\s+AND\s+')
#     ss = p.split(a)
#     print ss
# else :
#     if "AND " in a:
#         p = re.compile(r'\s+AND\s+')
#         ss = p.split(a)
#         print ss

