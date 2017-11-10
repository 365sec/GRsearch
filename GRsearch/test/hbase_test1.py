# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
import time
from elasticsearch import Elasticsearch
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from django.shortcuts import render, HttpResponse
from hbase import Hbase
from hbase.ttypes import *


transport = TSocket.TSocket('172.16.39.231', 9090)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
hbase_client = Hbase.Client(protocol)
transport.open()

hbase_client.deleteAllRow("t_wel_website", "6")