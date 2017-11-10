# -*- coding:utf-8 -*-

import json
import re
import urllib2
from elasticsearch import Elasticsearch



url = "http://180.97.185.130:9200/_cat/nodes?v&h=ip,disk.avail,heap.max,ram.max"
response = urllib2.urlopen(url)
content = response.read()
print content.split('\n')[0]
a = re.split('[\n]',content)
print a
i = 1
list1 = []
list2 = []
list3 = []
while i < (len(a)-1):
    res1 = re.search(r'\d*\.\d*\.\d*\.\d*\s*(?P<name1>[^\s]*)\s*(?P<name2>[^\s]*)\s*(?P<name3>[^\s]*)',a[i])
    list1.append(res1.group("name1"))
    list2.append(res1.group("name2"))
    list3.append(res1.group("name3"))
    i += 1
j = 0
print list1
print list2
print list3
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
    print str(disk_available_all)+"tb"
elif disk_available_all > 1:
    print str(disk_available_all)+"gb"
else:
    disk_available_all = disk_available_all/1024/1024
    print str(disk_available_all)+"mb"






















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

