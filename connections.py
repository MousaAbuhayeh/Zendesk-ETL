import logging.handlers
import requests
import pyodbc
import time
from static import zendesk_user,zendesk_pwd,native_client,sql_server,database,database_uid,database_pwd


#setting up smtp_handler
smtp_handler = logging.handlers.SMTPHandler(mailhost=("mail.smtp2go.com", 2525),
                                            fromaddr="Data@equiti.com",
                                            toaddrs="mousa.abuhayyeh@equiti.com",
                                            subject=u"Zendesk ETL!",
                                            credentials=("Data@equiti.com","CEC2p5Wy8SHZhuSB"),
                                            secure= ())


logger = logging.getLogger()
logger.addHandler(smtp_handler)

def get_response(url):
    response = requests.get(url, auth=(zendesk_user, zendesk_pwd))
    if response.status_code == 200:
        data = response.json()
        return data
    elif response.status_code == 429:
        time.sleep(int(response.headers['retry-after']))
        return get_response(url)
    else:
        logger.error(('Zendesk tickets ETL', 'Status:', response.status_code, 'Problem with the request. Exiting.'))
        exit()


def connect_to_sql_server():
    #connecting to target sql server
    cnxn_str = ("Driver={};"
                "Server={};"
                "Database={};"
                "UID={};"
                "PWD={};".format(native_client,sql_server,database,database_uid,database_pwd))
    try:
        target_cnxn = pyodbc.connect(cnxn_str)
    except:
        logger.exception('Target Connection ERROR!!')
        exit()
    target_cursor = target_cnxn.cursor()
    return target_cursor

def execute_sql_statement(is_insert_statement,cursor,sql_statement):
    try:
        cursor.execute(sql_statement)
    except:
        logger.exception('Zendesk tickets ETL query ERROR' + sql_statement)
        exit()
    if is_insert_statement == 1:
        cursor.commit()



def fetch_data(cursor):
    data = cursor.fetchall()
    return data

def send_report(msg):
    logger.error(msg)
