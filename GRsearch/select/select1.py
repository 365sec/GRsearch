# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
from elasticsearch import Elasticsearch

client = Elasticsearch("172.16.39.233:9200")

def search(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'select.html' , context)