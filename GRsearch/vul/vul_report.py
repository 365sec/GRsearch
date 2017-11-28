# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse
import json
import re
import MySQLdb

def vul_report(request):
    page = int(request.GET.get('page', '1'))
    vulnid = request.GET.get('vulnid','10001')
    current_page = page
    next_page = page+1
    last_page = page-1
    conn = MySQLdb.connect(host='172.16.39.99', user='es', passwd='`1q`1q', db='global_scan', port=3306, charset='utf8')
    cur = conn.cursor()
    sql_miaoshu = "select name,detail from t_vuln where vulnid = '"+vulnid+"'"  #获取漏洞名称，概述
    cur.execute(sql_miaoshu)
    miaoshu_data = cur.fetchall()
    vul_name = miaoshu_data[0][0]
    vul_miaoshu = miaoshu_data[0][1]
    sql_datanum = "select count(*) from t_vuln_globle where vulnid = '"+vulnid+"'"  #获取数据数目
    cur.execute(sql_datanum)
    data_num = cur.fetchall()
    total_nums = data_num[0][0]
    page_nums = int(total_nums / 100) + 1 if (page % 100) > 0 else int(total_nums / 100)
    page_list = [
                i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
            ]
    sql_country = "select country_name,count(*) from t_vuln_globle where vulnid = '"+vulnid+"' GROUP BY country_name ORDER BY count(*) DESC"
    cur.execute(sql_country)  #获取国家分布统计信息
    country_data = cur.fetchall()
    country_list = []
    max_count = country_data[0][1]
    country_name_list = []
    country_count_list = []
    for row in country_data:
        country_dict = {}
        country_dict["name"] = row[0]
        country_dict["value"] = int(row[1])
        country_list.append(country_dict)
        country_name_list.append(row[0])
        country_count_list.append(row[1])
    if len(country_name_list)>30:
        name_list = []
        count_list = []
        for i in range(0,30):#用做柱状图
            name_list.append(country_name_list[i])
            count_list.append(country_count_list[i])
    else:
        name_list = country_name_list
        count_list = country_count_list
    count_list = json.dumps(count_list, ensure_ascii=False)
    name_list = json.dumps(name_list,ensure_ascii=False)
    country_list = json.dumps(country_list, ensure_ascii=False) #用作地图的呈现
    country_list = country_list.replace('"{', '{')
    country_list = country_list.replace('}"', '}')
    country_list = country_list.replace('\\"', '"')
    sql_port = "select port,count(*) from t_vuln_globle where vulnid = '"+vulnid+"' GROUP BY port"
    cur.execute(sql_port)  #端口分布信息
    port_data = cur.fetchall()
    port_list = []
    port_name_list = []
    for row in port_data:
        port_dict = {}
        port_dict["name"] = row[0]
        port_dict["value"] = int(row[1])
        port_list.append(port_dict)
        port_name_list.append(row[0])
    port_list = json.dumps(port_list, ensure_ascii=False)
    port_list = port_list.replace('"{', '{')
    port_list = port_list.replace('}"', '}')
    port_list = port_list.replace('\\"', '"')
    sql_content = "select ip,country_name,scantime,city,region_name,port from t_vuln_globle where vulnid = '"+vulnid+"' limit " + str((page - 1) * 100) + ",100"
    cur.execute(sql_content)
    content = cur.fetchall()
    content_list = []
    country_code_dict = {  #用作前端提取国家图标
    "Canada": "CA",
    "Turkmenistan": "TM",
    "Cambodia": "KH",
    "Ethiopia": "ET",
    "Aruba": "AW",
    "Swaziland": "SZ",
    "Palestine": "PS",
    "Argentina": "AR",
    "Bolivia": "BO",
    "Cameroon": "CM",
    "Burkina Faso": "BF",
    "Ghana": "GH",
    "Saudi Arabia": "SA",
    "Bonaire, Sint Eustatius, and Saba": "BQ",
    "American Samoa": "AS",
    "Slovenia": "SI",
    "Guatemala": "GT",
    "Bosnia and Herzegovina": "BA",
    "Guinea": "GN",
    "Spain": "ES",
    "Liberia": "LR",
    "Netherlands": "NL",
    "Jamaica": "JM",
    "Oman": "OM",
    "Tanzania": "TZ",
    "Ivory Coast": "CI",
    "Isle of Man": "IM",
    "Gabon": "GA",
    "Monaco": "MC",
    "New Zealand": "NZ",
    "Yemen": "YE",
    "Pakistan": "PK",
    "Namibia": "NA",
    "Albania": "AL",
    "United Arab Emirates": "AE",
    "Guam": "GU",
    "Kosovo": "XK",
    "India": "IN",
    "Azerbaijan": "AZ",
    "Saint Vincent and the Grenadines": "VC",
    "Kenya": "KE",
    "Macao": "MO",
    "Greenland": "GL",
    "Turkey": "TR",
    "Afghanistan": "AF",
    "Fiji": "FJ",
    "Bangladesh": "BD",
    "Andorra": "AD",
    "Eritrea": "ER",
    "Saint Lucia": "LC",
    "Mongolia": "MN",
    "France": "FR",
    "Rwanda": "RW",
    "Slovakia": "SK",
    "Somalia": "SO",
    "Peru": "PE",
    "Laos": "LA",
    "Norway": "NO",
    "Malawi": "MW",
    "Cook Islands": "CK",
    "Benin": "BJ",
    "Singapore": "SG",
    "Montenegro": "ME",
    "Togo": "TG",
    "China": "CN",
    "Armenia": "AM",
    "Antigua and Barbuda": "AG",
    "Dominican Republic": "DO",
    "Ukraine": "UA",
    "Bahrain": "BH",
    "Finland": "FI",
    "Libya": "LY",
    "Indonesia": "ID",
    "United States": "US",
    "Tajikistan": "TJ",
    "Sweden": "SE",
    "Vietnam": "VN",
    "British Virgin Islands": "VG",
    "Mali": "ML",
    "East Timor": "TL",
    "Vatican City": "VA",
    "Russia": "RU",
    "Bulgaria": "BG",
    "Mauritius": "MU",
    "Romania": "RO",
    "Angola": "AO",
    "Portugal": "PT",
    "South Africa": "ZA",
    "Nicaragua": "NI",
    "Liechtenstein": "LI",
    "Qatar": "QA",
    "Malaysia": "MY",
    "Austria": "AT",
    "Mozambique": "MZ",
    "Uganda": "UG",
    "Hungary": "HU",
    "Niger": "NE",
    "Brazil": "BR",
    "Syria": "SY",
    "Faroe Islands": "FO",
    "Kuwait": "KW",
    "Panama": "PA",
    "Guyana": "GY",
    "Republic of Moldova": "MD",
    "Costa Rica": "CR",
    "Luxembourg": "LU",
    "Bahamas": "BS",
    "Gibraltar": "GI",
    "Ireland": "IE",
    "Hashemite Kingdom of Jordan": "JO",
    "Palau": "PW",
    "Nigeria": "NG",
    "Ecuador": "EC",
    "Brunei": "BN",
    "Australia": "AU",
    "Iran": "IR",
    "Algeria": "DZ",
    "Republic of Lithuania": "LT",
    "El Salvador": "SV",
    "Czechia": "CZ",
    "Gambia": "GM",
    "Marshall Islands": "MH",
    "Chile": "CL",
    "Puerto Rico": "PR",
    "Belgium": "BE",
    "Thailand": "TH",
    "Haiti": "HT",
    "Belize": "BZ",
    "Hong Kong": "HK",
    "Georgia": "GE",
    "Denmark": "DK",
    "Philippines": "PH",
    "French Guiana": "GF",
    "Morocco": "MA",
    "Croatia": "HR",
    "French Polynesia": "PF",
    "Guernsey": "GG",
    "Switzerland": "CH",
    "Grenada": "GD",
    "Myanmar [Burma]": "MM",
    "U.S. Virgin Islands": "VI",
    "Seychelles": "SC",
    "Estonia": "EE",
    "Uruguay": "UY",
    "Equatorial Guinea": "GQ",
    "Lebanon": "LB",
    "Uzbekistan": "UZ",
    "Tunisia": "TN",
    "Djibouti": "DJ",
    "Bermuda": "BM",
    "Republic of Korea": "KR",
    "Colombia": "CO",
    "Burundi": "BI",
    "Taiwan": "TW",
    "Cyprus": "CY",
    "Barbados": "BB",
    "Madagascar": "MG",
    "Italy": "IT",
    "Bhutan": "BT",
    "Sudan": "SD",
    "Nepal": "NP",
    "Malta": "MT",
    "Maldives": "MV",
    "Suriname": "SR",
    "Cayman Islands": "KY",
    "Anguilla": "AI",
    "Venezuela": "VE",
    "Israel": "IL",
    "R\u00e9union": "RE",
    "Iceland": "IS",
    "Zambia": "ZM",
    "Senegal": "SN",
    "Papua New Guinea": "PG",
    "Trinidad and Tobago": "TT",
    "Zimbabwe": "ZW",
    "Germany": "DE",
    "Vanuatu": "VU",
    "Martinique": "MQ",
    "Saint Martin": "MF",
    "Kazakhstan": "KZ",
    "Poland": "PL",
    "Mauritania": "MR",
    "Kyrgyzstan": "KG",
    "Mayotte": "YT",
    "Iraq": "IQ",
    "New Caledonia": "NC",
    "Macedonia": "MK",
    "Sri Lanka": "LK",
    "Latvia": "LV",
    "Japan": "JP",
    "Belarus": "BY",
    "Guadeloupe": "GP",
    "Honduras": "HN",
    "Mexico": "MX",
    "Egypt": "EG",
    "Cuba": "CU",
    "Serbia": "RS",
    "United Kingdom": "GB",
    "Congo": "CD",
    "Greece": "GR",
    "Paraguay": "PY",
    "Cura\u00e7ao": "CW",
    "Botswana": "BW"
}
    for row in content:
        content_dict = {}
        status = len(content_list)%2
        content_dict["status"] = status   #用于表格奇偶样式，0为奇，1为偶
        content_dict["ip"] = row[0]
        content_dict["country_name"] = row[1]
        content_dict["scantime"] = row[2]
        content_dict["port"] = row[5]
        if row[3] != None:
            content_dict["city"] = row[3]
        else:
            content_dict["city"] = ""
        content_dict["province"] = row[4]
        if country_code_dict.has_key(row[1]):
            content_dict["country_code"] = country_code_dict[row[1]]
        else:
            content_dict["country_code"] = ""
        content_list.append(content_dict)
    return render(request, 'vul_report.html', {
                                             "country_list": country_list,
                                             "name_list": name_list,
                                             "count_list": count_list,
                                             "port_list": port_list,
                                             "port_name_list": port_name_list,
                                             "country_name_list": country_name_list,
                                             "max_country_count": max_count,
                                             "content_list": content_list,
                                             "page_list": page_list,
                                             "page_nums": page_nums,
                                             "current_page": current_page,
                                             "next_page": next_page,
                                             "last_page": last_page,
                                             "vulnid": vulnid,
                                             "vul_name": vul_name,
                                             "vul_miaoshu": vul_miaoshu
                                             })
def vul_select(request):
    page = int(request.GET.get('page', '1'))
    current_page = page
    next_page = page+1
    last_page = page-1
    port = request.GET.get('port', '')
    vulnid = request.GET.get('vulnid','10001')
    country_name = request.GET.get('country_name','')
    conn = MySQLdb.connect(host='172.16.39.99', user='es', passwd='`1q`1q', db='global_scan', port=3306, charset='utf8')
    cur = conn.cursor()
    country_code_dict = {
    "Canada": "CA",
    "Turkmenistan": "TM",
    "Cambodia": "KH",
    "Ethiopia": "ET",
    "Aruba": "AW",
    "Swaziland": "SZ",
    "Palestine": "PS",
    "Argentina": "AR",
    "Bolivia": "BO",
    "Cameroon": "CM",
    "Burkina Faso": "BF",
    "Ghana": "GH",
    "Saudi Arabia": "SA",
    "Bonaire, Sint Eustatius, and Saba": "BQ",
    "American Samoa": "AS",
    "Slovenia": "SI",
    "Guatemala": "GT",
    "Bosnia and Herzegovina": "BA",
    "Guinea": "GN",
    "Spain": "ES",
    "Liberia": "LR",
    "Netherlands": "NL",
    "Jamaica": "JM",
    "Oman": "OM",
    "Tanzania": "TZ",
    "Ivory Coast": "CI",
    "Isle of Man": "IM",
    "Gabon": "GA",
    "Monaco": "MC",
    "New Zealand": "NZ",
    "Yemen": "YE",
    "Pakistan": "PK",
    "Namibia": "NA",
    "Albania": "AL",
    "United Arab Emirates": "AE",
    "Guam": "GU",
    "Kosovo": "XK",
    "India": "IN",
    "Azerbaijan": "AZ",
    "Saint Vincent and the Grenadines": "VC",
    "Kenya": "KE",
    "Macao": "MO",
    "Greenland": "GL",
    "Turkey": "TR",
    "Afghanistan": "AF",
    "Fiji": "FJ",
    "Bangladesh": "BD",
    "Andorra": "AD",
    "Eritrea": "ER",
    "Saint Lucia": "LC",
    "Mongolia": "MN",
    "France": "FR",
    "Rwanda": "RW",
    "Slovakia": "SK",
    "Somalia": "SO",
    "Peru": "PE",
    "Laos": "LA",
    "Norway": "NO",
    "Malawi": "MW",
    "Cook Islands": "CK",
    "Benin": "BJ",
    "Singapore": "SG",
    "Montenegro": "ME",
    "Togo": "TG",
    "China": "CN",
    "Armenia": "AM",
    "Antigua and Barbuda": "AG",
    "Dominican Republic": "DO",
    "Ukraine": "UA",
    "Bahrain": "BH",
    "Finland": "FI",
    "Libya": "LY",
    "Indonesia": "ID",
    "United States": "US",
    "Tajikistan": "TJ",
    "Sweden": "SE",
    "Vietnam": "VN",
    "British Virgin Islands": "VG",
    "Mali": "ML",
    "East Timor": "TL",
    "Vatican City": "VA",
    "Russia": "RU",
    "Bulgaria": "BG",
    "Mauritius": "MU",
    "Romania": "RO",
    "Angola": "AO",
    "Portugal": "PT",
    "South Africa": "ZA",
    "Nicaragua": "NI",
    "Liechtenstein": "LI",
    "Qatar": "QA",
    "Malaysia": "MY",
    "Austria": "AT",
    "Mozambique": "MZ",
    "Uganda": "UG",
    "Hungary": "HU",
    "Niger": "NE",
    "Brazil": "BR",
    "Syria": "SY",
    "Faroe Islands": "FO",
    "Kuwait": "KW",
    "Panama": "PA",
    "Guyana": "GY",
    "Republic of Moldova": "MD",
    "Costa Rica": "CR",
    "Luxembourg": "LU",
    "Bahamas": "BS",
    "Gibraltar": "GI",
    "Ireland": "IE",
    "Hashemite Kingdom of Jordan": "JO",
    "Palau": "PW",
    "Nigeria": "NG",
    "Ecuador": "EC",
    "Brunei": "BN",
    "Australia": "AU",
    "Iran": "IR",
    "Algeria": "DZ",
    "Republic of Lithuania": "LT",
    "El Salvador": "SV",
    "Czechia": "CZ",
    "Gambia": "GM",
    "Marshall Islands": "MH",
    "Chile": "CL",
    "Puerto Rico": "PR",
    "Belgium": "BE",
    "Thailand": "TH",
    "Haiti": "HT",
    "Belize": "BZ",
    "Hong Kong": "HK",
    "Georgia": "GE",
    "Denmark": "DK",
    "Philippines": "PH",
    "French Guiana": "GF",
    "Morocco": "MA",
    "Croatia": "HR",
    "French Polynesia": "PF",
    "Guernsey": "GG",
    "Switzerland": "CH",
    "Grenada": "GD",
    "Myanmar [Burma]": "MM",
    "U.S. Virgin Islands": "VI",
    "Seychelles": "SC",
    "Estonia": "EE",
    "Uruguay": "UY",
    "Equatorial Guinea": "GQ",
    "Lebanon": "LB",
    "Uzbekistan": "UZ",
    "Tunisia": "TN",
    "Djibouti": "DJ",
    "Bermuda": "BM",
    "Republic of Korea": "KR",
    "Colombia": "CO",
    "Burundi": "BI",
    "Taiwan": "TW",
    "Cyprus": "CY",
    "Barbados": "BB",
    "Madagascar": "MG",
    "Italy": "IT",
    "Bhutan": "BT",
    "Sudan": "SD",
    "Nepal": "NP",
    "Malta": "MT",
    "Maldives": "MV",
    "Suriname": "SR",
    "Cayman Islands": "KY",
    "Anguilla": "AI",
    "Venezuela": "VE",
    "Israel": "IL",
    "R\u00e9union": "RE",
    "Iceland": "IS",
    "Zambia": "ZM",
    "Senegal": "SN",
    "Papua New Guinea": "PG",
    "Trinidad and Tobago": "TT",
    "Zimbabwe": "ZW",
    "Germany": "DE",
    "Vanuatu": "VU",
    "Martinique": "MQ",
    "Saint Martin": "MF",
    "Kazakhstan": "KZ",
    "Poland": "PL",
    "Mauritania": "MR",
    "Kyrgyzstan": "KG",
    "Mayotte": "YT",
    "Iraq": "IQ",
    "New Caledonia": "NC",
    "Macedonia": "MK",
    "Sri Lanka": "LK",
    "Latvia": "LV",
    "Japan": "JP",
    "Belarus": "BY",
    "Guadeloupe": "GP",
    "Honduras": "HN",
    "Mexico": "MX",
    "Egypt": "EG",
    "Cuba": "CU",
    "Serbia": "RS",
    "United Kingdom": "GB",
    "Congo": "CD",
    "Greece": "GR",
    "Paraguay": "PY",
    "Cura\u00e7ao": "CW",
    "Botswana": "BW"
}
    if port != "":
        if country_name != "":
            sql_datanum = "select count(*) from t_vuln_globle where port = '"+port+"' and country_name = '"+country_name+"' and vulnid = '"+vulnid+"'"
            cur.execute(sql_datanum)
            data_num = cur.fetchall()
            total_nums = data_num[0][0]
            page_nums = int(total_nums / 100) + 1 if (page % 100) > 0 else int(total_nums / 100)
            page_list = [
                i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
            ]
            sql_content = "select ip,country_name,scantime,city,region_name,port from t_vuln_globle where port = '"+port+"' and country_name = '"+country_name+"' and vulnid = '"+vulnid+"' limit " + str((page - 1) * 100) + ",100 "
            cur.execute(sql_content)
            content = cur.fetchall()
            content_list = []
            for row in content:
                content_dict = {}
                status = len(content_list)%2
                content_dict["status"] = status   #用于表格奇偶样式，0为奇，1为偶
                content_dict["ip"] = row[0]
                content_dict["country_name"] = row[1]
                content_dict["scantime"] = str(row[2])
                content_dict["port"] = row[5]
                if row[3] != None:
                    content_dict["city"] = row[3]
                else:
                    content_dict["city"] = ""
                content_dict["province"] = row[4]
                if country_code_dict.has_key(row[1]):
                    content_dict["country_code"] = country_code_dict[row[1]]
                else:
                    content_dict["country_code"] = ""
                content_list.append(content_dict)
            response_content = {}
            response_content["page_nums"] = page_nums
            response_content["page_list"] = page_list
            response_content["current_page"] = current_page
            response_content["next_page"] = next_page
            response_content["last_page"] = last_page
            response_content["content_list"] = content_list
            response_content = json.dumps(response_content)
            return HttpResponse(response_content)
        else:
            sql_datanum = "select count(*) from t_vuln_globle where port = '"+port+"' and vulnid = '"+vulnid+"'"
            cur.execute(sql_datanum)
            data_num = cur.fetchall()
            total_nums = data_num[0][0]
            page_nums = int(total_nums / 100) + 1 if (page % 100) > 0 else int(total_nums / 100)
            page_list = [
                i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
            ]
            sql_content = "select ip,country_name,scantime,city,region_name,port from t_vuln_globle where port = '"+port+"' and vulnid = '"+vulnid+"' limit " + str((page - 1) * 100) + ",100 "
            cur.execute(sql_content)
            content = cur.fetchall()
            content_list = []
            for row in content:
                content_dict = {}
                status = len(content_list)%2
                content_dict["status"] = status   #用于表格奇偶样式，0为奇，1为偶
                content_dict["ip"] = row[0]
                content_dict["country_name"] = row[1]
                content_dict["scantime"] = str(row[2])
                content_dict["port"] = row[5]
                if row[3] != None:
                    content_dict["city"] = row[3]
                else:
                    content_dict["city"] = ""
                content_dict["province"] = row[4]
                if country_code_dict.has_key(row[1]):
                    content_dict["country_code"] = country_code_dict[row[1]]
                else:
                    content_dict["country_code"] = ""
                content_list.append(content_dict)
            response_content = {}
            response_content["page_nums"] = page_nums
            response_content["page_list"] = page_list
            response_content["current_page"] = current_page
            response_content["next_page"] = next_page
            response_content["last_page"] = last_page
            response_content["content_list"] = content_list
            response_content = json.dumps(response_content)
            return HttpResponse(response_content)
    else:
        if country_name != "":
            sql_datanum = "select count(*) from t_vuln_globle where country_name = '"+country_name+"' and vulnid = '"+vulnid+"'"
            cur.execute(sql_datanum)
            data_num = cur.fetchall()
            total_nums = data_num[0][0]
            page_nums = int(total_nums / 100) + 1 if (page % 100) > 0 else int(total_nums / 100)
            page_list = [
                i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
            ]
            sql_content = "select ip,country_name,scantime,city,region_name,port from t_vuln_globle where country_name = '"+country_name+"' and vulnid = '"+vulnid+"' limit " + str((page - 1) * 100) + ",100"
            cur.execute(sql_content)
            content = cur.fetchall()
            content_list = []
            for row in content:
                content_dict = {}
                status = len(content_list)%2
                content_dict["status"] = status   #用于表格奇偶样式，0为奇，1为偶
                content_dict["ip"] = row[0]
                content_dict["country_name"] = row[1]
                content_dict["scantime"] = str(row[2])
                content_dict["port"] = row[5]
                if row[3] != None:
                    content_dict["city"] = row[3]
                else:
                    content_dict["city"] = ""
                content_dict["province"] = row[4]
                if country_code_dict.has_key(row[1]):
                    content_dict["country_code"] = country_code_dict[row[1]]
                else:
                    content_dict["country_code"] = ""
                content_list.append(content_dict)
            response_content = {}
            response_content["page_nums"] = page_nums
            response_content["page_list"] = page_list
            response_content["current_page"] = current_page
            response_content["next_page"] = next_page
            response_content["last_page"] = last_page
            response_content["content_list"] = content_list
            response_content = json.dumps(response_content)
            return HttpResponse(response_content)
        else:
            sql_datanum = "select count(*) from t_vuln_globle where vulnid = '"+vulnid+"'"
            cur.execute(sql_datanum)
            data_num = cur.fetchall()
            total_nums = data_num[0][0]
            page_nums = int(total_nums / 100) + 1 if (page % 100) > 0 else int(total_nums / 100)
            page_list = [
                i for i in range(page - 4, page + 5) if 0 < i <= page_nums  # 分页页码列表
            ]
            sql_content = "select ip,country_name,scantime,city,region_name,port from t_vuln_globle where vulnid = '"+vulnid+"' limit " + str((page - 1) * 100) + ",100"
            cur.execute(sql_content)
            content = cur.fetchall()
            content_list = []
            for row in content:
                content_dict = {}
                status = len(content_list)%2
                content_dict["status"] = status   #用于表格奇偶样式，0为奇，1为偶
                content_dict["ip"] = row[0]
                content_dict["country_name"] = row[1]
                content_dict["scantime"] = str(row[2])
                content_dict["port"] = row[5]
                if row[3] != None:
                    content_dict["city"] = row[3]
                else:
                    content_dict["city"] = ""
                content_dict["province"] = row[4]
                if country_code_dict.has_key(row[1]):
                    content_dict["country_code"] = country_code_dict[row[1]]
                else:
                    content_dict["country_code"] = ""
                content_list.append(content_dict)
            response_content = {}
            response_content["page_nums"] = page_nums
            response_content["page_list"] = page_list
            response_content["current_page"] = current_page
            response_content["next_page"] = next_page
            response_content["last_page"] = last_page
            response_content["content_list"] = content_list
            response_content = json.dumps(response_content)
            return HttpResponse(response_content)
    