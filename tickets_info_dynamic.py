import time

from connections import get_response,connect_to_sql_server,execute_sql_statement
from sql_statements import sql_insert_into
from static import metric_sets_fields_list,metric_sets_columns_str,tickets_fields_list_ticket,tickets_fields_list_via_satisfaction,tickets_fields_list_lists,tickets_columns_str,ticket_update_url
from ndicts.ndicts import NestedDict

def update_tickets_info():
    cursor = connect_to_sql_server()
    url = ticket_update_url


    while url:
        data = get_response(url)
        id_str = ''
        metric_id_str = ''
        ticket_val_str = ''


        custom_val_str = ''
        custom_column_str = '"ticket_id"'
        i = 0

        metric_val_str = ''
        for ticket in data['tickets']:
            id_str += "'%s'," % ticket['id']
            ticket_val_str += "("
            # tickets first section
            for val in tickets_fields_list_ticket:
                if ticket[val] is None:
                    ticket_val_str += "NULL,"
                elif isinstance(ticket[val],str):
                    ticket_val_str += "N'%s'," % ticket[val].replace("'", "''")
                else:
                    ticket_val_str += "N'%s'," % ticket[val]

            #tickets via_satisfaction section
            nd = NestedDict(ticket)
            for val in tickets_fields_list_via_satisfaction:
                if val in nd:
                    if nd[val] is None:
                        ticket_val_str += "NULL,"
                    elif isinstance(nd[val],str):
                        ticket_val_str += "N'%s'," % nd[val].replace("'", "''")
                    else:
                        ticket_val_str += "N'%s'," % nd[val]
                else:
                    ticket_val_str += "NULL,"


            #tickets lists section

            for val in tickets_fields_list_lists:
                value = str(ticket[val])
                if value is None:
                    ticket_val_str += "NULL,"
                else:
                    ticket_val_str += "N'%s'," % value.replace("'", "''")

            ticket_val_str = ticket_val_str.strip(',')
            ticket_val_str += "),"


            #custom_fields section

            custom_val_str += "("
            custom_val_str += "N'%s'," % ticket['id']
            for custom in ticket['custom_fields']:
                if i == 0:
                    custom_column_str += ',"%s"' % custom['id']
                if custom['value'] is None or custom['value'] == '':
                    custom_val_str += "NULL,"
                elif isinstance(custom['value'], str):
                    custom_val_str += "N'%s'," % custom['value'].replace("'", "''")
                elif isinstance(custom['value'], list):
                    item_str = ','.join(custom['value'])
                    custom_val_str += "N'%s'," % item_str.replace("'", "''")
                else:
                    custom_val_str += "N'%s'," % custom['value']
            custom_val_str = custom_val_str.strip(',')
            custom_val_str += "),"
            i = 1

        #metric_sets section
        for metric in data['metric_sets']:
            metric_id_str += "'%s'," % metric['id']
            metric_val_str += "("
            #ticket metric sets

            for val in metric_sets_fields_list:
                if metric[val] is None:
                    metric_val_str += "NULL,"
                elif isinstance(metric[val], str):
                    metric_val_str += "N'%s'," % metric[val].replace("'", "''")
                elif isinstance(metric[val],dict):
                    if metric[val]['calendar'] is None:
                        metric_val_str += "NULL,"
                    else:
                        metric_val_str += "N'%s'," % metric[val]['calendar']
                    if metric[val]['business'] is None:   
                        metric_val_str += "NULL,"
                    else:
                        metric_val_str += "N'%s'," % metric[val]['business']
                else:
                    metric_val_str += "N'%s'," % metric[val]

            if 'reply_time_in_seconds' in metric:
                metric_val_str += "N'%s'," % metric['reply_time_in_seconds']['calendar']
            else:
                metric_val_str += "NULL,"

            metric_val_str = metric_val_str.strip(',')
            metric_val_str += "),"


        ticket_val_str = ticket_val_str.strip(',')
        custom_val_str = custom_val_str.strip(',')
        metric_val_str = metric_val_str.strip(',')
        id_str = id_str.strip(',')
        metric_id_str = metric_id_str.strip(',')

        #execute_sql_statement(1,cursor,sql_insert_into('zen_tickets',id_str,tickets_columns_str,ticket_val_str))
        #execute_sql_statement(1,cursor,sql_insert_into('zen_custom_fields', id_str, custom_column_str,custom_val_str,'ticket_id'))
        execute_sql_statement(1,cursor,sql_insert_into('zen_metric_sets', metric_id_str, metric_sets_columns_str, metric_val_str))

        if data['end_of_stream'] is True:
            url = None
        else:
            url = data['after_url']


