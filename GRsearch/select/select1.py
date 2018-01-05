# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse

def search(request):
    return render(request, 'select.html')