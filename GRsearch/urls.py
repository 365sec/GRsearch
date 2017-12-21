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
sys.path.append("GRsearch/app")
import portscan,ipv4,host,websites_detail
sys.path.append("GRsearch/ajax_test")
import ajax_test,ipv4_dashboard,websites_ajax,websites_dashboard
sys.path.append("GRsearch/select")
import select1
sys.path.append("GRsearch/main")
import main
sys.path.append("GRsearch/vul")
import vul_report,vul_report_list

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^scan$', portscan.search, name="scan"),
    url(r'^ipv4$', portscan.search, name="ipv4"),
    url(r'^host$', host.search, name="host"),
    url(r'^ajax_submit$', ajax_test.ipv4_aggs, name="ajax_submit"),
    url(r'^ajax_select$', ajax_test.ipv4_select, name="ajax_select"),
    url(r'^ipv4_dashboard$', ipv4_dashboard.ipv4_aggs, name="ipv4_dashboard"),
    url(r'^select$', select1.search,name="select"),
    url(r'^GRsearch$', main.main, name="main"),
    url(r'^vul/report$', vul_report.vul_report, name="vul_report"),
    url(r'^vul/report_list$', vul_report_list.vul_report_list, name="vul_report_list"),
    url(r'^vul/select$', vul_report.vul_select, name="vul_select"),
    url(r'^websites_aggs$', websites_ajax.websites_aggs, name="websites_aggs"),
    url(r'^websites_dashboard', websites_dashboard.websites_aggs, name="websites_dashboard"),
    url(r'^websites_select$', websites_ajax.websites_select, name="websites_select"),
    url(r'^websites_detail$', websites_detail.search, name="websites_detail"),
    url(r'', main.main, name="main")
    
]