
reg2 = re.compile(r'\s*:\s*')
search_list = reg2.split(search_content)
filter_field = "location."+search_list[0]+".raw"
filter_field_value = search_list[1]