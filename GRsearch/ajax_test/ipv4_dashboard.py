# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
from elasticsearch import Elasticsearch

client = Elasticsearch("172.16.39.233:9200")

def ipv4_aggs(request):
    search_content = request.GET.get('q', '')
    filter = request.GET.get('filter', '')
    # search_content = request.POST
    es_list = ["es", "elasticsearch", "9200"]
    es_china = ["es china", "elasticsearch china", "9200 china"]
    if filter == '':
      if search_content in es_china:
        aggs = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                        {
                                        "match": {
                                                "9200.http.get.headers.content_type": "json"
                                                }
                                        },
                                        {
                                            "match_phrase": {
                                                "9200.http.get.body": "You Know, for Search"
                                                    }
                                               },
                                         {
                                          "match": {
                                                    "location.country": "china"
                                                    }
                                          }
                                        ]
                                    }
                                  },
                        "aggs": {
                            "country": {
                                "terms": {
                                    "field": "location.country.raw",
                                    "size": 50,
                                    "shard_size": 1000
                                        }
                                    },
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        signal1 = 0
        province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
        country_chinese_name_list = {           "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡",      "Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
        country_list = []
        for bucket in aggs["aggregations"]["country"]["buckets"]: 
            if bucket["key"] != "":
                country_dict = {}
                if(bucket["key"] in country_chinese_name_list.keys()):
                    country_dict["name"]=country_chinese_name_list[bucket["key"]]
                else:
                    country_dict["name"]=bucket["key"]
                country_dict["value"]=bucket["doc_count"]
                country_list.append(country_dict)
            else:
                signal1 += 1
        province_list = []
        signal2 = 0
        for bucket in aggs["aggregations"]["province"]["buckets"]:
            if bucket["key"] != "":
                province_dict = {}
                if(bucket["key"] in province_chinese_name_list.keys()):
                    province_dict["name"]=province_chinese_name_list[bucket["key"]]
                else:
                    province_dict["name"]=bucket["key"]
                province_dict["value"]=bucket["doc_count"]
                province_list.append(province_dict)
            else :
                signal2 += 1
        city_list = []
        signal3 = 0
        for bucket in aggs["aggregations"]["city"]["buckets"]:
            if bucket["key"] != "":
                city_dict = {}
                city_dict["name"] = bucket["key"]
                city_dict["value"] = bucket["doc_count"]
                city_list.append(city_dict)
            else:
                signal3 += 1
        aggs_content = {}
        aggs_content["china_province_list"] = province_list
        aggs_content["country_list"] = country_list
        aggs_content["province_list"] = province_list
        aggs_content["city_list"] = city_list
        result = json.dumps(aggs_content)
        return HttpResponse(result)
      elif search_content in es_list:
        aggs = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                        {
                                        "match": {
                                                "9200.http.get.headers.content_type": "json"
                                                }
                                        },
                                        {
                                            "match_phrase": {
                                                "9200.http.get.body": "You Know, for Search"
                                                    }
                                               }
                                        ]
                                    }
                                  },
                        "aggs": {
                            "country": {
                                "terms": {
                                    "field": "location.country.raw",
                                    "size": 50,
                                    "shard_size": 1000
                                        }
                                    },
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        country_list = []
        signal1 = 0
        province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
        country_chinese_name_list = {                 "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡","Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
        for bucket in aggs["aggregations"]["country"]["buckets"]: 
            if bucket["key"] != "":
                country_dict = {}
                if(bucket["key"] in country_chinese_name_list.keys()):
                    country_dict["name"]=country_chinese_name_list[bucket["key"]]
                else:
                    country_dict["name"]=bucket["key"]
                country_dict["value"]=bucket["doc_count"]
                country_list.append(country_dict)
            else:
                signal1 += 1
        province_list = []
        signal2 = 0
        for bucket in aggs["aggregations"]["province"]["buckets"]:
            if bucket["key"] != "":
                province_dict = {}
                if(bucket["key"] in province_chinese_name_list.keys()):
                    province_dict["name"]=province_chinese_name_list[bucket["key"]]
                else:
                    province_dict["name"]=bucket["key"]
                province_dict["value"]=bucket["doc_count"]
                province_list.append(province_dict)
            else :
                signal2 += 1
        city_list = []
        signal3 = 0
        for bucket in aggs["aggregations"]["city"]["buckets"]:
            if bucket["key"] != "":
                city_dict = {}
                city_dict["name"] = bucket["key"]
                city_dict["value"] = bucket["doc_count"]
                city_list.append(city_dict)
            else:
                signal3 += 1
        aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                        {
                                        "match": {
                                                "9200.http.get.headers.content_type": "json"
                                                }
                                        },
                                        {
                                            "match_phrase": {
                                                "9200.http.get.body": "You Know, for Search"
                                                    }
                                               },
                                         {
                                            "match":{
                                                     "location.country": "china"
                                                     }
                                          }
                                        ]
                                    }
                                  },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        china_province_list = []
        signal2 = 0
        for bucket in aggs1["aggregations"]["province"]["buckets"]:
            if bucket["key"] != "":
                province_dict = {}
                if(bucket["key"] in province_chinese_name_list.keys()):
                    province_dict["name"]=province_chinese_name_list[bucket["key"]]
                else:
                    province_dict["name"]=bucket["key"]
                province_dict["value"] = bucket["doc_count"]
                china_province_list.append(province_dict)    
            else :
                signal2 += 1
#         china_city_list = []
#         signal3 = 0
#         for bucket in aggs1["aggregations"]["city"]["buckets"]:
#             if bucket["key"] != "":
#                 china_city_dict = {}
#                 china_city_dict["name"] = bucket["key"]
#                 china_city_dict["value"] = bucket["doc_count"]
#                 china_city_list.append(china_city_dict)
#             else:
#                 signal3 += 1
        aggs_content = {}
        aggs_content["country_list"] = country_list
        aggs_content["province_list"] = province_list
        aggs_content["city_list"] = city_list
        aggs_content["china_province_list"] = china_province_list
        result = json.dumps(aggs_content)
        return HttpResponse(result)
      elif ":" in search_content:
        if "AND" in search_content:
            reg1 = re.compile(r'\s+AND\s+')  # 分割查询语句
            search_list = reg1.split(search_content)
            reg2 = re.compile(r'\s*:\s*')
            search_1_list = reg2.split(search_list[0])
            search_2_list = reg2.split(search_list[1])
            field1 = search_1_list[0]
            field1_value = search_1_list[1]
            field2 = search_2_list[0]
            field2_value = search_2_list[1]
            aggs = client.search(
                                 index="ipv4",
                                 doc_type="ipv4host",
                                 body={
                                     "size": 0,
                                     "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                         },
                                     "aggs": {
                                          "country": {
                                             "terms": {
                                                "field": "location.country.raw",
                                                "size": 11,
                                                "shard_size": 1000
                                                  }
                                               },
                                         "province":{
                                              "terms": {
                                                 "field": "location.province.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                    }
                                                },
                                         "city":{
                                             "terms": {
                                                 "field": "location.city.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                }
                                            }
                                          }
                                   }
                                 )
            country_list = []
            signal1 = 0
            province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
            country_chinese_name_list = {                 "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡","Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
            for bucket in aggs["aggregations"]["country"]["buckets"]: 
                if bucket["key"] != "":
                    country_dict = {}
                    if(bucket["key"] in country_chinese_name_list.keys()):
                        country_dict["name"]=country_chinese_name_list[bucket["key"]]
                    else:
                        country_dict["name"]=bucket["key"]
                    country_dict["value"]=bucket["doc_count"]
                    country_list.append(country_dict)
                else:
                    signal1 += 1
            province_list = []
            signal2 = 0
            for bucket in aggs["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    province_dict["name"] = bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    province_list.append(province_dict)    
                else :
                    signal2 += 1
            city_list = []
            signal3 = 0
            for bucket in aggs["aggregations"]["city"]["buckets"]:
                if bucket["key"] != "":
                    city_dict = {}
                    city_dict["name"] = bucket["key"]
                    city_dict["value"] = bucket["doc_count"]
                    city_list.append(city_dict)
                else:
                    signal3 += 1
            aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                        
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      },
                                         {
                                            "match":{
                                                     "location.country": "china"
                                                     }
                                          }
                                        ]
                                    }
                                  },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
            china_province_list = []
            signal2 = 0
            for bucket in aggs1["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    china_province_list.append(province_dict)    
                else :
                    signal2 += 1
#             china_city_list = []
#             signal3 = 0
#             for bucket in aggs1["aggregations"]["city"]["buckets"]:
#                 if bucket["key"] != "":
#                     china_city_dict = {}
#                     china_city_dict["name"] = bucket["key"]
#                     china_city_dict["value"] = bucket["doc_count"]
#                     china_city_list.append(china_city_dict)
#                 else:
#                     signal3 += 1
            aggs_content = {}
            aggs_content["country_list"] = country_list
            aggs_content["province_list"] = province_list
            aggs_content["city_list"] = city_list
            aggs_content["china_province_list"] = china_province_list
            result = json.dumps(aggs_content)
            return HttpResponse(result)
        elif "OR" in search_content:
            reg1 = re.compile(r'\s+OR\s+')  # 分割查询语句
            search_list = reg1.split(search_content)
            reg2 = re.compile(r'\s*:\s*')
            search_1_list = reg2.split(search_list[0])
            search_2_list = reg2.split(search_list[1])
            field1 = search_1_list[0]
            field1_value = search_1_list[1]
            field2 = search_2_list[0]
            field2_value = search_2_list[1]  
            aggs = client.search(
                                index="ipv4",
                                doc_type="ipv4host",
                                body={
                                     "size": 0,
                                     "query": {
                                        "bool": {
                                            "should": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                                 }
                                         },
                                     "aggs": {
                                          "country": {
                                             "terms": {
                                                "field": "location.country.raw",
                                                "size": 11,
                                                "shard_size": 1000
                                                  }
                                               },
                                         "province":{
                                              "terms": {
                                                 "field": "location.province.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                    }
                                                },
                                         "city":{
                                             "terms": {
                                                 "field": "location.city.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                }
                                            }
                                          }
                                       }
                                     )
            country_list = []
            signal1 = 0
            province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
            country_chinese_name_list = {                 "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡","Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
            for bucket in aggs["aggregations"]["country"]["buckets"]: 
                if bucket["key"] != "":
                    country_dict = {}
                    if(bucket["key"] in country_chinese_name_list.keys()):
                        country_dict["name"]=country_chinese_name_list[bucket["key"]]
                    else:
                        country_dict["name"]=bucket["key"]
                    country_dict["value"]=bucket["doc_count"]
                    country_list.append(country_dict)
                else:
                    signal1 += 1
            province_list = []
            signal2 = 0
            for bucket in aggs["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    province_dict["name"] = bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    province_list.append(province_dict)    
                else :
                    signal2 += 1
            city_list = []
            signal3 = 0
            for bucket in aggs["aggregations"]["city"]["buckets"]:
                if bucket["key"] != "":
                    city_dict = {}
                    city_dict["name"] = bucket["key"]
                    city_dict["value"] = bucket["doc_count"]
                    city_list.append(city_dict)
                else:
                    signal3 += 1
            aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                         {
                                            "match":{
                                                     "location.country": "china"
                                                     }
                                          }
                                        ],
                                "should": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ]
                                    }
                                  },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
            china_province_list = []
            signal2 = 0
            for bucket in aggs1["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    china_province_list.append(province_dict)    
                else :
                    signal2 += 1
#             china_city_list = []
#             signal3 = 0
#             for bucket in aggs1["aggregations"]["city"]["buckets"]:
#                 if bucket["key"] != "":
#                     china_city_dict = {}
#                     china_city_dict["name"] = bucket["key"]
#                     china_city_dict["value"] = bucket["doc_count"]
#                     china_city_list.append(china_city_dict)
#                 else:
#                     signal3 += 1
            aggs_content = {}
            aggs_content["country_list"] = country_list
            aggs_content["province_list"] = province_list
            aggs_content["city_list"] = city_list
            aggs_content["china_province_list"] = china_province_list
            result = json.dumps(aggs_content)
            return HttpResponse(result)
        elif "NOT" in search_content:
            reg1 = re.compile(r'\s+NOT\s+')  # 分割查询语句
            search_list = reg1.split(search_content)
            reg2 = re.compile(r'\s*:\s*')
            search_1_list = reg2.split(search_list[0])
            search_2_list = reg2.split(search_list[1])
            field1 = search_1_list[0]
            field1_value = search_1_list[1]
            field2 = search_2_list[0]
            field2_value = search_2_list[1]
            aggs = client.search(
                                index="ipv4",
                                doc_type="ipv4host",
                                body={
                                     "size": 0,
                                     "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ]
                                                 }
                                           },
                                     "aggs": {
                                          "country": {
                                             "terms": {
                                                "field": "location.country.raw",
                                                "size": 11,
                                                "shard_size": 1000
                                                  }
                                               },
                                         "province":{
                                              "terms": {
                                                 "field": "location.province.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                    }
                                                },
                                         "city":{
                                             "terms": {
                                                 "field": "location.city.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                }
                                            }
                                          }
                                       }
                                     )
            country_list = []
            signal1 = 0
            province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
            country_chinese_name_list = {                 "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡","Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
            for bucket in aggs["aggregations"]["country"]["buckets"]: 
                if bucket["key"] != "":
                    country_dict = {}
                    if(bucket["key"] in country_chinese_name_list.keys()):
                        country_dict["name"]=country_chinese_name_list[bucket["key"]]
                    else:
                        country_dict["name"]=bucket["key"]
                    country_dict["value"]=bucket["doc_count"]
                    country_list.append(country_dict)
                else:
                    signal1 += 1
            province_list = []
            signal2 = 0
            for bucket in aggs["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    province_dict["name"] = bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    province_list.append(province_dict)    
                else :
                    signal2 += 1
            city_list = []
            signal3 = 0
            for bucket in aggs["aggregations"]["city"]["buckets"]:
                if bucket["key"] != "":
                    city_dict = {}
                    city_dict["name"] = bucket["key"]
                    city_dict["value"] = bucket["doc_count"]
                    city_list.append(city_dict)
                else:
                    signal3 += 1
            aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                    {
                                                     "match":{
                                                              "location.country": "china"
                                                              }
                                                     }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ]
                                    }
                                  },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
            china_province_list = []
            signal2 = 0
            for bucket in aggs1["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    china_province_list.append(province_dict)    
                else :
                    signal2 += 1
#             china_city_list = []
#             signal3 = 0
#             for bucket in aggs1["aggregations"]["city"]["buckets"]:
#                 if bucket["key"] != "":
#                     china_city_dict = {}
#                     china_city_dict["name"] = bucket["key"]
#                     china_city_dict["value"] = bucket["doc_count"]
#                     china_city_list.append(china_city_dict)
#                 else:
#                     signal3 += 1
            aggs_content = {}
            aggs_content["country_list"] = country_list
            aggs_content["province_list"] = province_list
            aggs_content["city_list"] = city_list
            aggs_content["china_province_list"] = china_province_list
            result = json.dumps(aggs_content)
            return HttpResponse(result)
        else:
            reg2 = re.compile(r'\s*:\s*')
            search_list = reg2.split(search_content)
            field1 = search_list[0]
            field1_value = search_list[1]
            aggs = client.search(
                                 index="ipv4",
                                 doc_type="ipv4host",
                                 body={
                                     "size": 0,
                                     "query": {
                                        "match": {
                                            field1: field1_value
                                                 }
                                         },
                                     "aggs": {
                                          "country": {
                                             "terms": {
                                                "field": "location.country.raw",
                                                "size": 11,
                                                "shard_size": 1000
                                                  }
                                               },
                                         "province":{
                                              "terms": {
                                                 "field": "location.province.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                    }
                                                },
                                         "city":{
                                             "terms": {
                                                 "field": "location.city.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                }
                                            }
                                          }
                                   }
                                 )
            country_list = []
            signal1 = 0
            province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
            country_chinese_name_list = {                 "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡","Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
            for bucket in aggs["aggregations"]["country"]["buckets"]: 
                if bucket["key"] != "":
                    country_dict = {}
                    if(bucket["key"] in country_chinese_name_list.keys()):
                        country_dict["name"]=country_chinese_name_list[bucket["key"]]
                    else:
                        country_dict["name"]=bucket["key"]
                    country_dict["value"]=bucket["doc_count"]
                    country_list.append(country_dict)
                else:
                    signal1 += 1
            province_list = []
            signal2 = 0
            for bucket in aggs["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    province_dict["name"] = bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    province_list.append(province_dict)    
                else :
                    signal2 += 1
            city_list = []
            signal3 = 0
            for bucket in aggs["aggregations"]["city"]["buckets"]:
                if bucket["key"] != "":
                    city_dict = {}
                    city_dict["name"] = bucket["key"]
                    city_dict["value"] = bucket["doc_count"]
                    city_list.append(city_dict)
                else:
                    signal3 += 1
            aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                    {
                                                     "match":{
                                                              "location.country": "china"
                                                              }
                                                     }
                                                     ]
                                    }
                                  },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
            china_province_list = []
            signal2 = 0
            for bucket in aggs1["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    china_province_list.append(province_dict)    
                else :
                    signal2 += 1
#             china_city_list = []
#             signal3 = 0
#             for bucket in aggs1["aggregations"]["city"]["buckets"]:
#                 if bucket["key"] != "":
#                     china_city_dict = {}
#                     china_city_dict["name"] = bucket["key"]
#                     china_city_dict["value"] = bucket["doc_count"]
#                     china_city_list.append(china_city_dict)
#                 else:
#                     signal3 += 1
            aggs_content = {}
            aggs_content["country_list"] = country_list
            aggs_content["province_list"] = province_list
            aggs_content["city_list"] = city_list
            aggs_content["china_province_list"] = china_province_list
            result = json.dumps(aggs_content)
            return HttpResponse(result)
      else:
        aggs = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                        {
                                        "match": {
                                                "_all": search_content
                                                }
                                        }
                                        ]
                                    }
                                  },
                        "aggs": {
                            "country": {
                                "terms": {
                                    "field": "location.country.raw",
                                    "size": 11,
                                    "shard_size": 1000
                                        }
                                    },
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        country_list = []
        signal1 = 0
        province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
        country_chinese_name_list = {                 "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡","Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
        for bucket in aggs["aggregations"]["country"]["buckets"]: 
            if bucket["key"] != "":
                country_dict = {}
                if(bucket["key"] in country_chinese_name_list.keys()):
                    country_dict["name"]=country_chinese_name_list[bucket["key"]]
                else:
                    country_dict["name"]=bucket["key"]
                country_dict["value"]=bucket["doc_count"]
                country_list.append(country_dict)
            else:
                signal1 += 1
        province_list = []
        signal2 = 0
        for bucket in aggs["aggregations"]["province"]["buckets"]:
            if bucket["key"] != "":
                province_dict = {}
                province_dict["name"] = bucket["key"]
                province_dict["value"] = bucket["doc_count"]
                province_list.append(province_dict)    
            else :
                signal2 += 1
        city_list = []
        signal3 = 0
        for bucket in aggs["aggregations"]["city"]["buckets"]:
            if bucket["key"] != "":
                city_dict = {}
                city_dict["name"] = bucket["key"]
                city_dict["value"] = bucket["doc_count"]
                city_list.append(city_dict)
            else:
                signal3 += 1
        aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                            "bool": {
                                "must": [
                                        {
                                        "match": {
                                                "_all": search_content
                                                }
                                        },
                                         {
                                            "match":{
                                                     "location.country": "china"
                                                     }
                                          }
                                        ]
                                    }
                                  },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        china_province_list = []
        signal2 = 0
        for bucket in aggs1["aggregations"]["province"]["buckets"]:
            if bucket["key"] != "":
                province_dict = {}
                if(bucket["key"] in province_chinese_name_list.keys()):
                    province_dict["name"]=province_chinese_name_list[bucket["key"]]
                else:
                    province_dict["name"]=bucket["key"]
                province_dict["value"] = bucket["doc_count"]
                china_province_list.append(province_dict)    
            else :
                signal2 += 1
#         china_city_list = []
#         signal3 = 0
#         for bucket in aggs1["aggregations"]["city"]["buckets"]:
#             if bucket["key"] != "":
#                 china_city_dict = {}
#                 china_city_dict["name"] = bucket["key"]
#                 china_city_dict["value"] = bucket["doc_count"]
#                 china_city_list.append(china_city_dict)
#             else:
#                 signal3 += 1
        aggs_content = {}
        aggs_content["country_list"] = country_list
        aggs_content["province_list"] = province_list
        aggs_content["city_list"] = city_list
        aggs_content["china_province_list"] = china_province_list
        result = json.dumps(aggs_content)
        return HttpResponse(result)
    else:
      reg2 = re.compile(r'\s*:\s*')
      search_list = reg2.split(filter)
      filter_field = "location." + search_list[0] + ".raw"
      filter_field_value = search_list[1]
      if search_content in es_china:
        aggs = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                                        "bool": {
                                            "must": [
                                                   {
                                                    "match": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    },
                                                    {
                                                       "match":{
                                                           "location.country": "china"
                                                         }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         },
                        "aggs": {
                            "country": {
                                "terms": {
                                    "field": "location.country.raw",
                                    "size": 11,
                                    "shard_size": 1000
                                        }
                                    },
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        country_list = []
        signal1 = 0
        province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
        country_chinese_name_list = {             "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡",    "Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
        for bucket in aggs["aggregations"]["country"]["buckets"]: 
            if bucket["key"] != "":
                country_dict = {}
                if(bucket["key"] in country_chinese_name_list.keys()):
                    country_dict["name"]=country_chinese_name_list[bucket["key"]]
                else:
                    country_dict["name"]=bucket["key"]
                country_dict["value"]=bucket["doc_count"]
                country_list.append(country_dict)
            else:
                signal1 += 1
        if signal1 == 0:  # 除判断是否包含""，还需判断长度是否为11
            if len(country_list) > 10:
                country_list.pop()
        province_list = []
        signal2 = 0
        for bucket in aggs["aggregations"]["province"]["buckets"]:
            if bucket["key"] != "":
                province_dict = {}
                if(bucket["key"] in province_chinese_name_list.keys()):
                    province_dict["name"]=province_chinese_name_list[bucket["key"]]
                else:
                    province_dict["name"]=bucket["key"]
                province_dict["value"]=bucket["doc_count"]
                province_list.append(province_dict)
            else :
                signal2 += 1
        if signal2 == 0:
            if len(province_list) > 10:
                province_list.pop()
        city_list = []
        signal3 = 0
        for bucket in aggs["aggregations"]["city"]["buckets"]:
            if bucket["key"] != "":
                city_dict = {}
                city_dict["name"] = bucket["key"]
                city_dict["value"] = bucket["doc_count"]
                city_list.append(city_dict)
            else:
                signal3 += 1
        if signal3 == 0:
            if len(city_list) > 10:
                city_list.pop()
        aggs_content = {}
        aggs_content["country_list"] = country_list
        aggs_content["province_list"] = province_list
        aggs_content["chinese_province_list"] = province_list
        aggs_content["city_list"] = city_list
        result = json.dumps(aggs_content)
        return HttpResponse(result)
      elif search_content in es_list:
        aggs = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                                        "bool": {
                                            "must": [
                                                   {
                                                    "match": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         },
                        "aggs": {
                            "country": {
                                "terms": {
                                    "field": "location.country.raw",
                                    "size": 11,
                                    "shard_size": 1000
                                        }
                                    },
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        country_list = []
        signal1 = 0
        province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
        country_chinese_name_list = {        "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡",         "Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
        for bucket in aggs["aggregations"]["country"]["buckets"]: 
            if bucket["key"] != "":
                country_dict = {}
                if(bucket["key"] in country_chinese_name_list.keys()):
                    country_dict["name"]=country_chinese_name_list[bucket["key"]]
                else:
                    country_dict["name"]=bucket["key"]
                country_dict["value"]=bucket["doc_count"]
                country_list.append(country_dict)
            else:
                signal1 += 1
        if signal1 == 0:  # 除判断是否包含""，还需判断长度是否为11
            if len(country_list) > 10:
                country_list.pop()
        province_list = []
        signal2 = 0
        for bucket in aggs["aggregations"]["province"]["buckets"]:
            if bucket["key"] != "":
                province_dict = {}
                if(bucket["key"] in province_chinese_name_list.keys()):
                    province_dict["name"]=province_chinese_name_list[bucket["key"]]
                else:
                    province_dict["name"]=bucket["key"]
                province_dict["value"]=bucket["doc_count"]
                province_list.append(province_dict)
            else :
                signal2 += 1
        if signal2 == 0:
            if len(province_list) > 10:
                province_list.pop()
        city_list = []
        signal3 = 0
        for bucket in aggs["aggregations"]["city"]["buckets"]:
            if bucket["key"] != "":
                city_dict = {}
                city_dict["name"] = bucket["key"]
                city_dict["value"] = bucket["doc_count"]
                city_list.append(city_dict)
            else:
                signal3 += 1
        if signal3 == 0:
            if len(city_list) > 10:
                city_list.pop()
        aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                                        "bool": {
                                            "must": [
                                                   {
                                                    "match": {
                                                        "9200.http.get.headers.content_type": "json"
                                                         }
                                                    },
                                                   {
                                                     "match_phrase": {
                                                         "9200.http.get.body": "You Know, for Search"
                                                         }
                                                    },
                                                    {
                                                       "match":{
                                                           "location.country": "china"
                                                         }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        china_province_list = []
        signal2 = 0
        for bucket in aggs1["aggregations"]["province"]["buckets"]:
            if bucket["key"] != "":
                province_dict = {}
                if(bucket["key"] in province_chinese_name_list.keys()):
                    province_dict["name"]=province_chinese_name_list[bucket["key"]]
                else:
                    province_dict["name"]=bucket["key"]
                province_dict["value"] = bucket["doc_count"]
                china_province_list.append(province_dict)    
            else :
                signal2 += 1
        aggs_content = {}
        aggs_content["country_list"] = country_list
        aggs_content["province_list"] = province_list
        aggs_content["china_province_list"] = china_province_list
        aggs_content["city_list"] = city_list
        result = json.dumps(aggs_content)
        return HttpResponse(result)
      elif ":" in search_content:
        if "AND" in search_content:
            reg1 = re.compile(r'\s+AND\s+')  # 分割查询语句
            search_list = reg1.split(search_content)
            reg2 = re.compile(r'\s*:\s*')
            search_1_list = reg2.split(search_list[0])
            search_2_list = reg2.split(search_list[1])
            field1 = search_1_list[0]
            field1_value = search_1_list[1]
            field2 = search_2_list[0]
            field2_value = search_2_list[1]
            aggs = client.search(
                                 index="ipv4",
                                 doc_type="ipv4host",
                                 body={
                                     "size": 0,
                                     "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                             "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         },
                                     "aggs": {
                                          "country": {
                                             "terms": {
                                                "field": "location.country.raw",
                                                "size": 11,
                                                "shard_size": 1000
                                                  }
                                               },
                                         "province":{
                                              "terms": {
                                                 "field": "location.province.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                    }
                                                },
                                         "city":{
                                             "terms": {
                                                 "field": "location.city.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                }
                                            }
                                          }
                                   }
                                 )
            country_list = []
            signal1 = 0
            province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
            country_chinese_name_list = {         "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡",        "Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
            for bucket in aggs["aggregations"]["country"]["buckets"]: 
                if bucket["key"] != "":
                    country_dict = {}
                    if(bucket["key"] in country_chinese_name_list.keys()):
                        country_dict["name"]=country_chinese_name_list[bucket["key"]]
                    else:
                        country_dict["name"]=bucket["key"]
                    country_dict["value"]=bucket["doc_count"]
                    country_list.append(country_dict)
                else:
                    signal1 += 1
            if signal1 == 0:
                if len(country_list) > 10:
                    country_list.pop()
            province_list = []
            signal2 = 0
            for bucket in aggs["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"]=bucket["doc_count"]
                    province_list.append(province_dict)
                else :
                    signal2 += 1
            if signal2 == 0:
                if len(province_list) > 10:
                    province_list.pop()
            city_list = []
            signal3 = 0
            for bucket in aggs["aggregations"]["city"]["buckets"]:
                if bucket["key"] != "":
                    city_dict = {}
                    city_dict["name"] = bucket["key"]
                    city_dict["value"] = bucket["doc_count"]
                    city_list.append(city_dict)
                else:
                    signal3 += 1
            if signal3 == 0:
                if len(city_list) > 10:
                    city_list.pop()
            aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                                        "bool": {
                                            "must": [
                                                   {
                                                    "match": {
                                                        field1: field1_value
                                                         }
                                                    },
                                                   {
                                                     "match": {
                                                         field2: field2_value
                                                         }
                                                    }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
            china_province_list = []
            signal2 = 0
            for bucket in aggs1["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    china_province_list.append(province_dict)    
                else :
                    signal2 += 1
            aggs_content = {}
            aggs_content["china_province_list"] = china_province_list        
            aggs_content["country_list"] = country_list
            aggs_content["province_list"] = province_list
            aggs_content["city_list"] = city_list
            result = json.dumps(aggs_content)
            return HttpResponse(result)
        elif "OR" in search_content:
            reg1 = re.compile(r'\s+OR\s+')  # 分割查询语句
            search_list = reg1.split(search_content)
            reg2 = re.compile(r'\s*:\s*')
            search_1_list = reg2.split(search_list[0])
            search_2_list = reg2.split(search_list[1])
            field1 = search_1_list[0]
            field1_value = search_1_list[1]
            field2 = search_2_list[0]
            field2_value = search_2_list[1]  
            aggs = client.search(
                                index="ipv4",
                                doc_type="ipv4host",
                                body={
                                     "size": 0,
                                     "query": {
                                        "bool": {
                                            "should": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                           },
                                     "aggs": {
                                          "country": {
                                             "terms": {
                                                "field": "location.country.raw",
                                                "size": 11,
                                                "shard_size": 1000
                                                  }
                                               },
                                         "province":{
                                              "terms": {
                                                 "field": "location.province.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                    }
                                                },
                                         "city":{
                                             "terms": {
                                                 "field": "location.city.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                }
                                            }
                                          }
                                       }
                                     )
            country_list = []
            signal1 = 0
            province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
            country_chinese_name_list = {           "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡",      "Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
            for bucket in aggs["aggregations"]["country"]["buckets"]: 
                if bucket["key"] != "":
                    country_dict = {}
                    if(bucket["key"] in country_chinese_name_list.keys()):
                        country_dict["name"]=country_chinese_name_list[bucket["key"]]
                    else:
                        country_dict["name"]=bucket["key"]
                    country_dict["value"]=bucket["doc_count"]
                    country_list.append(country_dict)
                else:
                    signal1 += 1
            if signal1 == 0:
                if len(country_list) > 10:
                    country_list.pop()
            province_list = []
            signal2 = 0
            for bucket in aggs["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"]=bucket["doc_count"]
                    province_list.append(province_dict)
                else :
                    signal2 += 1
            if signal2 == 0:
                if len(province_list) > 10:
                    province_list.pop()
            city_list = []
            signal3 = 0
            for bucket in aggs["aggregations"]["city"]["buckets"]:
                if bucket["key"] != "":
                    city_dict = {}
                    city_dict["name"] = bucket["key"]
                    city_dict["value"] = bucket["doc_count"]
                    city_list.append(city_dict)
                else:
                    signal3 += 1
            if signal3 == 0:
                if len(city_list) > 10:
                    city_list.pop()
            aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                                        "bool": {
                                            "must": [
                                                   {
                                                    "match": {
                                                        "location.country": "china"
                                                         }
                                                    }
                                                     ],
                                            "should": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
            china_province_list = []
            signal2 = 0
            for bucket in aggs1["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    china_province_list.append(province_dict)    
                else :
                    signal2 += 1
            aggs_content = {}
            aggs_content["china_province_list"] = china_province_list  
            aggs_content["country_list"] = country_list
            aggs_content["province_list"] = province_list
            aggs_content["city_list"] = city_list
            result = json.dumps(aggs_content)
            return HttpResponse(result)
        elif "NOT" in search_content:
            reg1 = re.compile(r'\s+NOT\s+')  # 分割查询语句
            search_list = reg1.split(search_content)
            reg2 = re.compile(r'\s*:\s*')
            search_1_list = reg2.split(search_list[0])
            search_2_list = reg2.split(search_list[1])
            field1 = search_1_list[0]
            field1_value = search_1_list[1]
            field2 = search_2_list[0]
            field2_value = search_2_list[1]
            aggs = client.search(
                                index="ipv4",
                                doc_type="ipv4host",
                                body={
                                     "size": 0,
                                     "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                         ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                           },
                                     "aggs": {
                                          "country": {
                                             "terms": {
                                                "field": "location.country.raw",
                                                "size": 11,
                                                "shard_size": 1000
                                                  }
                                               },
                                         "province":{
                                              "terms": {
                                                 "field": "location.province.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                    }
                                                },
                                         "city":{
                                             "terms": {
                                                 "field": "location.city.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                }
                                            }
                                          }
                                       }
                                     )
            country_list = []
            signal1 = 0
            province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
            country_chinese_name_list = {        "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡",         "Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
            for bucket in aggs["aggregations"]["country"]["buckets"]: 
                if bucket["key"] != "":
                    country_dict = {}
                    if(bucket["key"] in country_chinese_name_list.keys()):
                        country_dict["name"]=country_chinese_name_list[bucket["key"]]
                    else:
                        country_dict["name"]=bucket["key"]
                    country_dict["value"]=bucket["doc_count"]
                    country_list.append(country_dict)
                else:
                    signal1 += 1
            if signal1 == 0:
                if len(country_list) > 10:
                    country_list.pop()
            province_list = []
            signal2 = 0
            for bucket in aggs["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"]=bucket["doc_count"]
                    province_list.append(province_dict)
                else :
                    signal2 += 1
            if signal2 == 0:
                if len(province_list) > 10:
                    province_list.pop()
            city_list = []
            signal3 = 0
            for bucket in aggs["aggregations"]["city"]["buckets"]:
                if bucket["key"] != "":
                    city_dict = {}
                    city_dict["name"] = bucket["key"]
                    city_dict["value"] = bucket["doc_count"]
                    city_list.append(city_dict)
                else:
                    signal3 += 1
            if signal3 == 0:
                if len(city_list) > 10:
                    city_list.pop()
            aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                                        "bool": {
                                            "must": [
                                                    {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                   {
                                                    "match": {
                                                        "location.country": "china"
                                                         }
                                                    }
                                                     ],
                                            "must_not": [
                                                     {
                                                      "match":{
                                                               field2 : field2_value
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
            china_province_list = []
            signal2 = 0
            for bucket in aggs1["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    china_province_list.append(province_dict)    
                else :
                    signal2 += 1
            aggs_content = {}
            aggs_content["china_province_list"] = china_province_list 
            aggs_content["country_list"] = country_list
            aggs_content["province_list"] = province_list
            aggs_content["city_list"] = city_list
            result = json.dumps(aggs_content)
            return HttpResponse(result)
        else:
            reg2 = re.compile(r'\s*:\s*')
            search_list = reg2.split(search_content)
            field1 = search_list[0]
            field1_value = search_list[1]
            aggs = client.search(
                                 index="ipv4",
                                 doc_type="ipv4host",
                                 body={
                                     "size": 0,
                                     "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                }
                                            },
                                     "aggs": {
                                          "country": {
                                             "terms": {
                                                "field": "location.country.raw",
                                                "size": 11,
                                                "shard_size": 1000
                                                  }
                                               },
                                         "province":{
                                              "terms": {
                                                 "field": "location.province.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                    }
                                                },
                                         "city":{
                                             "terms": {
                                                 "field": "location.city.raw",
                                                 "size": 11,
                                                 "shard_size": 1000
                                                }
                                            }
                                          }
                                   }
                                 )
            country_list = []
            signal1 = 0
            province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
            country_chinese_name_list = {         "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡",        "Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
            for bucket in aggs["aggregations"]["country"]["buckets"]: 
                if bucket["key"] != "":
                    country_dict = {}
                    if(bucket["key"] in country_chinese_name_list.keys()):
                        country_dict["name"]=country_chinese_name_list[bucket["key"]]
                    else:
                        country_dict["name"]=bucket["key"]
                    country_dict["value"]=bucket["doc_count"]
                    country_list.append(country_dict)
                else:
                    signal1 += 1
            if signal1 == 0:
                if len(country_list) > 10:
                    country_list.pop()
            province_list = []
            signal2 = 0
            for bucket in aggs["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"]=bucket["doc_count"]
                    province_list.append(province_dict)
                else :
                    signal2 += 1
            if signal2 == 0:
                if len(province_list) > 10:
                    province_list.pop()
            city_list = []
            signal3 = 0
            for bucket in aggs["aggregations"]["city"]["buckets"]:
                if bucket["key"] != "":
                    city_dict = {}
                    city_dict["name"] = bucket["key"]
                    city_dict["value"] = bucket["doc_count"]
                    city_list.append(city_dict)
                else:
                    signal3 += 1
            if signal3 == 0:
                if len(city_list) > 10:
                    city_list.pop()
            aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                                        "bool": {
                                            "must": [
                                                    {
                                                      "match":{
                                                               field1 : field1_value
                                                               }
                                                      },
                                                   {
                                                    "match": {
                                                        "location.country": "china"
                                                         }
                                                    }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
            china_province_list = []
            signal2 = 0
            for bucket in aggs1["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"] = bucket["doc_count"]
                    china_province_list.append(province_dict)    
                else :
                    signal2 += 1
            aggs_content = {}
            aggs_content["china_province_list"] = china_province_list 
            aggs_content["country_list"] = country_list
            aggs_content["province_list"] = province_list
            aggs_content["city_list"] = city_list
            result = json.dumps(aggs_content)
            return HttpResponse(result)
      else:
        aggs = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                                        "bool": {
                                            "must": [
                                                     {
                                                      "match":{
                                                               "_all" : search_content
                                                               }
                                                      }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                }
                                            },
                        "aggs": {
                            "country": {
                                "terms": {
                                    "field": "location.country.raw",
                                    "size": 11,
                                    "shard_size": 1000
                                        }
                                    },
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 11,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        country_list = []
        signal1 = 0
        province_chinese_name_list = {     "Zhejiang":"浙江",     "Beijing":"北京",     "Guangdong":"广东",     "Shanghai":"上海",     "Jiangsu":"江苏",     "Sichuan":"四川",     "Fujian":"福建",     "Hunan":"湖南",     "Henan":"河南",     "Shandong":"山东",     "Liaoning":"辽宁",     "Jiangxi":"江西",     "Anhui":"安徽",     "Shaanxi":"陕西",     "Hebei":"河北",     "Gansu":"甘肃",     "Chongqing":"重庆",     "Hubei":"湖北",     "Tianjin":"天津",     "Yunnan":"云南",     "Jilin":"吉林",     "Shanxi":"山西",     "Heilongjiang":"黑龙江",     "Guangxi":"广西",     "Xinjiang":"新疆",     "Guizhou":"贵州",     "Inner Mongolia Autonomous Region":"内蒙古",     "Hainan":"海南",     "Ningsia Hui Autonomous Region":"宁夏",     "Qinghai":"青海",     "Tibet":"西藏" }
        country_chinese_name_list = {      "Republic of Korea":"韩国","United States":"美国","Singapore":"新加坡",           "Afghanistan":"阿富汗",                 "Angola":"安哥拉",                 "Albania":"阿尔巴尼亚",                 "United Arab Emirates":"阿联酋",                 "Argentina":"阿根廷",                 "Armenia":"亚美尼亚",                 "French Southern and Antarctic Lands":"法属南半球和南极领地",                 "Australia":"澳大利亚",                 "Austria":"奥地利",                 "Azerbaijan":"阿塞拜疆",                 "Burundi":"布隆迪",                 "Belgium":"比利时",                 "Benin":"贝宁",                 "Burkina Faso":"布基纳法索",                 "Bangladesh":"孟加拉国",                 "Bulgaria":"保加利亚",                 "The Bahamas":"巴哈马",                 "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",                 "Belarus":"白俄罗斯",                 "Belize":"伯利兹",                 "Bermuda":"百慕大",                 "Bolivia":"玻利维亚",                 "Brazil":"巴西",                 "Brunei":"文莱",                 "Bhutan":"不丹",                 "Botswana":"博茨瓦纳",                 "Central African Republic":"中非共和国",                 "Canada":"加拿大",                 "Switzerland":"瑞士",                 "Chile":"智利",                 "China":"中国",                 "Ivory Coast":"象牙海岸",                 "Cameroon":"喀麦隆",                 "Democratic Republic of the Congo":"刚果民主共和国",                 "Republic of the Congo":"刚果共和国",                 "Colombia":"哥伦比亚",                 "Costa Rica":"哥斯达黎加",                 "Cuba":"古巴",                 "Northern Cyprus":"北塞浦路斯",                 "Cyprus":"塞浦路斯",                 "Czech Republic":"捷克共和国",                 "Germany":"德国",                 "Djibouti":"吉布提",                 "Denmark":"丹麦",                 "Dominican Republic":"多明尼加共和国",                 "Algeria":"阿尔及利亚",                 "Ecuador":"厄瓜多尔",                 "Egypt":"埃及",                 "Eritrea":"厄立特里亚",                 "Spain":"西班牙",                 "Estonia":"爱沙尼亚",                 "Ethiopia":"埃塞俄比亚",                 "Finland":"芬兰",                 "Fiji":"斐",                 "Falkland Islands":"福克兰群岛",                 "France":"法国",                 "Gabon":"加蓬",                 "United Kingdom":"英国",                 "Georgia":"格鲁吉亚",                 "Ghana":"加纳",                 "Guinea":"几内亚",                 "Gambia":"冈比亚",                 "Guinea Bissau":"几内亚比绍",                 "Equatorial Guinea":"赤道几内亚",                 "Greece":"希腊",                 "Greenland":"格陵兰",                 "Guatemala":"危地马拉",                 "French Guiana":"法属圭亚那",                 "Guyana":"圭亚那",                 "Honduras":"洪都拉斯",                 "Croatia":"克罗地亚",                 "Haiti":"海地",                 "Hungary":"匈牙利",                 "Indonesia":"印尼",                 "India":"印度",                 "Ireland":"爱尔兰",                 "Iran":"伊朗",                 "Iraq":"伊拉克",                 "Iceland":"冰岛",                 "Israel":"以色列",                 "Italy":"意大利",                 "Jamaica":"牙买加",                 "Jordan":"约旦",                 "Japan":"日本",                 "Kazakhstan":"哈萨克斯坦",                 "Kenya":"肯尼亚",                 "Kyrgyzstan":"吉尔吉斯斯坦",                 "Cambodia":"柬埔寨",                 "South Korea":"韩国",                 "Kosovo":"科索沃",                 "Kuwait":"科威特",                 "Laos":"老挝",                 "Lebanon":"黎巴嫩",                 "Liberia":"利比里亚",                 "Libya":"利比亚",                 "Sri Lanka":"斯里兰卡",                 "Lesotho":"莱索托",                 "Lithuania":"立陶宛",                 "Luxembourg":"卢森堡",                 "Latvia":"拉脱维亚",                 "Morocco":"摩洛哥",                 "Moldova":"摩尔多瓦",                 "Madagascar":"马达加斯加",                 "Mexico":"墨西哥",                 "Macedonia":"马其顿",                 "Mali":"马里",                 "Myanmar":"缅甸",                 "Montenegro":"黑山",                 "Mongolia":"蒙古",                 "Mozambique":"莫桑比克",                 "Mauritania":"毛里塔尼亚",                 "Malawi":"马拉维",                 "Malaysia":"马来西亚",                 "Namibia":"纳米比亚",                 "New Caledonia":"新喀里多尼亚",                 "Niger":"尼日尔",                 "Nigeria":"尼日利亚",                 "Nicaragua":"尼加拉瓜",                 "Netherlands":"荷兰",                 "Norway":"挪威",                 "Nepal":"尼泊尔",                 "New Zealand":"新西兰",                 "Oman":"阿曼",                 "Pakistan":"巴基斯坦",                 "Panama":"巴拿马",                 "Peru":"秘鲁",                 "Philippines":"菲律宾",                 "Papua New Guinea":"巴布亚新几内亚",                 "Poland":"波兰",                 "Puerto Rico":"波多黎各",                 "North Korea":"北朝鲜",                 "Portugal":"葡萄牙",                 "Paraguay":"巴拉圭",                 "Qatar":"卡塔尔",                 "Romania":"罗马尼亚",                 "Russia":"俄罗斯",                 "Rwanda":"卢旺达",                 "Western Sahara":"西撒哈拉",                 "Saudi Arabia":"沙特阿拉伯",                 "Sudan":"苏丹",                 "South Sudan":"南苏丹",                 "Senegal":"塞内加尔",                 "Solomon Islands":"所罗门群岛",                 "Sierra Leone":"塞拉利昂",                 "El Salvador":"萨尔瓦多",                 "Somaliland":"索马里兰",                 "Somalia":"索马里",                 "Republic of Serbia":"塞尔维亚共和国",                 "Suriname":"苏里南",                 "Slovakia":"斯洛伐克",                 "Slovenia":"斯洛文尼亚",                 "Sweden":"瑞典",                 "Swaziland":"斯威士兰",                 "Syria":"叙利亚",                 "Chad":"乍得",                 "Togo":"多哥",                 "Thailand":"泰国",                 "Tajikistan":"塔吉克斯坦",                 "Turkmenistan":"土库曼斯坦",                 "East Timor":"东帝汶",                 "Trinidad and Tobago":"特里尼达和多巴哥",                 "Tunisia":"突尼斯",                 "Turkey":"土耳其",                 "United Republic of Tanzania":"坦桑尼亚联合共和国",                 "Uganda":"乌干达",                 "Ukraine":"乌克兰",                 "Uruguay":"乌拉圭",                 "United States of America":"美国",                 "Uzbekistan":"乌兹别克斯坦",                 "Venezuela":"委内瑞拉",                 "Vietnam":"越南",                 "Vanuatu":"瓦努阿图",                 "West Bank":"西岸",                 "Yemen":"也门",                 "South Africa":"南非",                 "Zambia":"赞比亚",                 "Zimbabwe":"津巴布韦"             }
        for bucket in aggs["aggregations"]["country"]["buckets"]: 
            if bucket["key"] != "":
                country_dict = {}
                if(bucket["key"] in country_chinese_name_list.keys()):
                    country_dict["name"]=country_chinese_name_list[bucket["key"]]
                else:
                    country_dict["name"]=bucket["key"]
                country_dict["value"]=bucket["doc_count"]
                country_list.append(country_dict)
            else:
                signal1 += 1
        if signal1 == 0:  # 除判断是否包含""，还需判断长度是否为11
            if len(country_list) > 10:
                country_list.pop()
        province_list = []
        signal2 = 0
        for bucket in aggs["aggregations"]["province"]["buckets"]:
                if bucket["key"] != "":
                    province_dict = {}
                    if(bucket["key"] in province_chinese_name_list.keys()):
                        province_dict["name"]=province_chinese_name_list[bucket["key"]]
                    else:
                        province_dict["name"]=bucket["key"]
                    province_dict["value"]=bucket["doc_count"]
                    province_list.append(province_dict)
                else :
                    signal2 += 1
        if signal2 == 0:
            if len(province_list) > 10:
                province_list.pop()
        city_list = []
        signal3 = 0
        for bucket in aggs["aggregations"]["city"]["buckets"]:
            if bucket["key"] != "":
                city_dict = {}
                city_dict["name"] = bucket["key"]
                city_dict["value"] = bucket["doc_count"]
                city_list.append(city_dict)
            else:
                signal3 += 1
        if signal3 == 0:
            if len(city_list) > 10:
                city_list.pop()
        aggs1 = client.search(
                index="ipv4",
                doc_type="ipv4host",
                body={
                        "size": 0,
                        "query": {
                                        "bool": {
                                            "must": [
                                                    {
                                                      "match":{
                                                               "_all" : search_content
                                                               }
                                                      },
                                                   {
                                                    "match": {
                                                        "location.country": "china"
                                                         }
                                                    }
                                                     ],
                                            "filter": {
                                                       "term":{
                                                            filter_field : filter_field_value
                                                               }
                                                       }
                                                 }
                                         },
                        "aggs": {
                            "province":{
                                    "terms": {
                                        "field": "location.province.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                        }
                                    },
                            "city":{
                                "terms": {
                                        "field": "location.city.raw",
                                        "size": 50,
                                        "shard_size": 1000
                                            }
                                        }
                                    }
                                }
                            )
        china_province_list = []
        signal2 = 0
        for bucket in aggs1["aggregations"]["province"]["buckets"]:
            if bucket["key"] != "":
                province_dict = {}
                if(bucket["key"] in province_chinese_name_list.keys()):
                    province_dict["name"]=province_chinese_name_list[bucket["key"]]
                else:
                    province_dict["name"]=bucket["key"]
                province_dict["value"] = bucket["doc_count"]
                china_province_list.append(province_dict)    
            else :
                signal2 += 1
        aggs_content = {}
        aggs_content["china_province_list"] = china_province_list 
        aggs_content["country_list"] = country_list
        aggs_content["province_list"] = province_list
        aggs_content["city_list"] = city_list
        result = json.dumps(aggs_content)
        return HttpResponse(result)  