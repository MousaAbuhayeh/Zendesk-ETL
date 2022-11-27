from connections import get_response,connect_to_sql_server,execute_sql_statement,fetch_data
from sql_statements import sql_insert_into,sql_list_columns,sql_create_columns
from static import base_url


def check_create_custom_fields():

    #base ticket data
    url = base_url
    data = get_response(url)


    #target sql table columns
    cursor = connect_to_sql_server()
    execute_sql_statement(0,cursor,sql_list_columns('zen_custom_fields'))
    sql_data = fetch_data(cursor)
    new_list = [row.COLUMN_NAME for row in sql_data]



    #matching and creating columns_types_str
    columns_types_str = ''
    new_columns_count = 0
    for field in data['ticket']['custom_fields']:
        if str(field['id']) not in new_list:
            columns_types_str += "[%s] [nvarchar](max),"%field['id']
            new_columns_count += 1

    if new_columns_count > 0:
        columns_types_str = columns_types_str.strip(',')
        execute_sql_statement(1,cursor,sql_create_columns('zen_custom_fields',columns_types_str))
        return 'new columns added:'+columns_types_str
    else:
        return 'no new columns'



def update_maps(url,main_key,table_name,column_str,fields_list):

    cursor = connect_to_sql_server()

    #fetching ticket fields, users, groups data
    while url:
        data = get_response(url)
        for row in data[main_key]:
            values_str = ''
            for key in fields_list:
                if isinstance(row[key], str):
                    values_str += "N'%s'," % row[key].replace("'", "''")
                else:
                    values_str += "N'%s'," % row[key]
            values_str = values_str.strip(',')
            values_str = values_str.replace("N'None'", "NULL")
            execute_sql_statement(1, cursor, sql_insert_into(table_name,row['id'],column_str,values_str))

        if main_key == 'users':
            if data['end_of_stream'] is True:
                url = None
            else:
                url = data['after_url']
        else:
            if data['next_page'] is None:
                url = None
            else:
                url = data['next_page']

