import time
from custom_fields_dynamic import check_create_custom_fields,update_maps
from static import map_url_list,main_key_list,table_name_list,column_str_list,fields_list_list
from tickets_info_dynamic import update_tickets_info

st = time.time()

#--first section (ticket_fields insert,custom_fields check/create_new)

print(check_create_custom_fields())

#--update mapping tables(ticket_fields,groups,users)

for i, val in enumerate(map_url_list):
    update_maps(map_url_list[i],main_key_list[i],table_name_list[i],column_str_list[i],fields_list_list[i])

#--update tickets info(tickets,metric_sets,custom_fields)

#update_tickets_info()

et = time.time()
print(et-st)





