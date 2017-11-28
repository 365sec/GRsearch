# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse
import MySQLdb

def vul_report_list(request):
    conn = MySQLdb.connect(host="172.16.39.99",user="es",passwd="`1q`1q",db="global_scan",port=3306,charset="utf8")
    cur = conn.cursor()
    sql_vul = "select vulnid,name,detail from t_vuln"
    cur.execute(sql_vul)
    vul_data = cur.fetchall()
    vul_list = []
    for row in vul_data:
        vul_dict = {}
        vul_dict["vulnid"] = row[0]
        vul_dict["name"] = row[1]
        vul_dict["detail"] = row[2]
        vul_list.append(vul_dict)
    return render(request,'vul_report_list.html',{
                                                  "vul_list": vul_list
                                                  })