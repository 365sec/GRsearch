"""GRsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import sys
sys.path.append("GRsearch/search1")
import response
sys.path.append("GRsearch/app")
import view1,fenye,portscan,ipv4,host,portscan_detail,waf_detail,tsgz,waf_suyuan,waf_suyuan_filter,waf_suyuan_detail
sys.path.append("GRsearch/ajax_test")
import ajax_test,portscan_ajax,ipv4_dashboard,waf_ajax,waf_dashboard,waf_map
sys.path.append("GRsearch/select")
import select1
sys.path.append("GRsearch/main")
import main
sys.path.append("GRsearch/vul")
import vul_report,vul_report_list

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^response1/$', response.response),
    url(r'^search/$', view1.search ,name="search"),
    url(r'^fenye/$', fenye.search, name="fenye"),
    url(r'^scan/$', portscan.search, name="scan"),
    url(r'^ipv4/$', portscan.search, name="ipv4"),
    url(r'^host/$', host.search, name="host"),
    url(r'^ajax_test/$', ajax_test.search, name="ajax_test"),
    url(r'^ajax_submit/$', ajax_test.ipv4_aggs, name="ajax_submit"),
    url(r'^ajax_select/$', ajax_test.ipv4_select, name="ajax_select"),
    url(r'^ipv4_dashboard/$', ipv4_dashboard.ipv4_aggs, name="ipv4_dashboard"),
    url(r'^portscan_aggs/$', portscan_ajax.portscan_aggs, name="portscan_aggs"),
    url(r'^portscan_select/$', portscan_ajax.portscan_select, name="portscan_select"),
    url(r'^portscan_detail/$', portscan_detail.search, name="portscan_detail"),
    url(r'^select/$', select1.search,name="select"),
    url(r'^waf_ajax/$', waf_ajax.waf_aggs,name="waf_ajax"),
    url(r'^waf_select/$', waf_ajax.select,name="waf_select"),
    url(r'^waf_dashboard/$', waf_dashboard.waf_aggs,name="waf_dashboard"),
    url(r'^waf/$', waf_detail.search, name="waf"),
    url(r'^waf_map/$', waf_map.waf_aggs, name="waf_map"),
    url(r'^tsgz/$', tsgz.tsgz, name="tsgz"),
    url(r'^waf_suyuan/$', waf_suyuan.search, name="waf_suyuan"),
    url(r'^waf_suyuan/waf_suyuan_filter/$', waf_suyuan_filter.search, name="waf_suyuan_filter"),
    url(r'^waf_suyuan/waf_suyuan_detail/$', waf_suyuan_detail.detail, name="waf_suyuan_detail"),
    url(r'^GRsearch$', main.main, name="main"),
    url(r'^vul/report$', vul_report.vul_report, name="vul_report"),
    url(r'^vul/report_list$', vul_report_list.vul_report_list, name="vul_report_list"),
    url(r'^vul/select$', vul_report.vul_select, name="vul_select"),
    url(r'', main.main, name="main")
    
]
