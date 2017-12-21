# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
from elasticsearch import Elasticsearch

def main(request):
    return render(request,'main.html')