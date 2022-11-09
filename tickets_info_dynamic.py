from connections import get_response,connect_to_sql_server,execute_sql_statement,fetch_data
from sql_statements import sql_insert_into,sql_list_columns
from static import metric_sets_fields_list,metric_sets_columns_str,tickets_fields_list_ticket,tickets_fields_list_via_satisfaction,tickets_fields_list_lists,tickets_columns_str
from ndicts.ndicts import NestedDict

def update_tickets_info():
    cursor = connect_to_sql_server()
    url = 'https://equiti-helpdesk.zendesk.com/api/v2/incremental/tickets/cursor.json?per_page=1000&include=metric_sets,comment_count&start_time='+str(int(time.time())-100000)


    while url:
        data = get_response(url)


        for ticket in data['tickets']:
            values_str = ''
            # tickets first section
            for val in tickets_fields_list_ticket:
                if isinstance(ticket[val],str):
                    values_str += "N'%s'," % ticket[val].replace("'", "''")
                else:
                    values_str += "N'%s'," % ticket[val]

            #tickets via_satisfaction section
            nd = NestedDict(ticket)
            for val in tickets_fields_list_via_satisfaction:
                if val in nd:
                    if isinstance(nd[val],str):
                        values_str += "N'%s'," % nd[val].replace("'", "''")
                    else:
                        values_str += "N'%s'," % nd[val]
                else:
                    values_str += "N'None',"


            #tickets lists section

            for val in tickets_fields_list_lists:
                value = str(ticket[val])
                values_str += "N'%s'," % value.replace("'", "''")


            values_str = values_str.strip(',')
            values_str = values_str.replace("N'None'", "NULL")
            execute_sql_statement(1, cursor,sql_insert_into('zen_tickets', ticket['id'], tickets_columns_str, values_str))



            #custom_fields section
            values_str = ''
            custom_column_str = '"ticket_id"'
            values_str += "N'%s'," % ticket['id']
            for custom in ticket['custom_fields']:
                custom_column_str += ',"%s"' % custom['id']
                if custom['value'] is None or custom['value'] == '':
                    values_str += "N'None',"
                elif isinstance(custom['value'], str):
                    values_str += "N'%s'," % custom['value'].replace("'", "''")
                elif isinstance(custom['value'], list):
                    item_str = ','.join(custom['value'])
                    values_str += "N'%s'," % item_str.replace("'", "''")
                else:
                    values_str += "N'%s'," % custom['value']

            values_str = values_str.strip(',')
            values_str = values_str.replace("N'None'", "NULL")
            execute_sql_statement(1, cursor,sql_insert_into('zen_custom_fields', ticket['id'], custom_column_str, values_str,'ticket_id'))

        #metric_sets section
        for metric in data['metric_sets']:
            #ticket metric sets
            values_str = ''
            for val in metric_sets_fields_list:
                if isinstance(metric[val],dict):
                    values_str += "N'%s'," % metric[val]['calendar']
                    values_str += "N'%s'," % metric[val]['business']
                else:
                    values_str += "N'%s'," % metric[val]

            if 'reply_time_in_seconds' in metric:
                values_str += "N'%s'," % metric['reply_time_in_seconds']['calendar']
            else:
                values_str += "N'None',"

            values_str = values_str.strip(',')
            values_str = values_str.replace("N'None'", "NULL")
            execute_sql_statement(1, cursor, sql_insert_into('zen_metric_sets', metric['id'], metric_sets_columns_str, values_str))
        if data['end_of_stream'] is True:
            url = None
        else:
            url = data['after_url']


