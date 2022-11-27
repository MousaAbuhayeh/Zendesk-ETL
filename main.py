import time
from datetime import date

from connections import send_report
from custom_fields_dynamic import check_create_custom_fields,update_maps
from static import mapping_dict
from tickets_info_dynamic import update_tickets_info



st = time.time()

#--first section (ticket_fields insert,custom_fields check/create_new)

custom_fields_added = check_create_custom_fields()

#--update mapping tables(ticket_fields,groups,users)
    
for key in mapping_dict:    
    update_maps(mapping_dict[key]['url'],key,mapping_dict[key]['table_name'],
                mapping_dict[key]['column_str'],mapping_dict[key]['field_list'])

#--update tickets info(tickets,metric_sets,custom_fields)

update_tickets_info()

et = time.time()

runtime = et - st
msg = '''
Zendesk ETL Completion report :
Zendesk Process completed within {} seconds for {}
New custom fields result : {}'''.format(runtime,date.today(),custom_fields_added)

send_report(msg)






