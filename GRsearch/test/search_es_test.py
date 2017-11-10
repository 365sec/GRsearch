# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
from elasticsearch import Elasticsearch

client = Elasticsearch("172.16.39.233:9200")
response = client.get(index="liuren", id="11", doc_type="waf_log")
print response