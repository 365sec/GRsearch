# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse

def main(request):
    return render(request,'main.html')