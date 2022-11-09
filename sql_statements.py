#list of sql statement to be used with proper EXECUTE functions and server connections in main

#returns sql statement when executed will insert/delete records into sql table
def sql_insert_into(table_name,id,columns_str,values_str, column_name='id'):

    sql_statement='''
        Declare @id nvarchar(50);
        SET @id ='{}';IF EXISTS (SELECT 1 from dbo.{} WHERE {} = @id)
        BEGIN
        DELETE FROM dbo.{} WHERE {} = @id;
        INSERT INTO dbo.{} ({}) VALUES({});END
        ELSE
        BEGIN
        INSERT INTO dbo.{} ({}) VALUES({});END'''.format(id,table_name,column_name,table_name,column_name,table_name,columns_str,values_str,table_name,columns_str,values_str)

    return sql_statement

#returns sql statement when executed lists all columns in sql table
def sql_list_columns(table_name):

    sql_statement='''
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = N'{}' '''.format(table_name)

    return sql_statement


#returns sql statement when executed creates columns in sql table
def sql_create_columns(table_name,columns_types_str):

    sql_statement='''
    ALTER TABLE dbo.{}
    ADD {};'''.format(table_name,columns_types_str)
    return sql_statement



