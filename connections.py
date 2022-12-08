import os
import configparser
import logging.handlers
import requests
import pyodbc
import time

def read_config():
    cfg = configparser.ConfigParser(os.environ)
    directory = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(directory, 'config.ini')
    cfg.read(config_path)
    return cfg

cfg = read_config()


#setting up smtp_handler
smtp_handler = logging.handlers.SMTPHandler(mailhost=("mail.smtp2go.com", 2525),
                                            fromaddr="Data@equiti.com",
                                            toaddrs=("mousa.abuhayyeh@equiti.com","Data@equiti.com"),
                                            subject=u"Zendesk ETL!",
                                            credentials=("Data@equiti.com",cfg.get('smtp','password')),
                                            secure= ())


logger = logging.getLogger()
logger.addHandler(smtp_handler)

def get_response(url):
    response = requests.get(url, auth=(cfg.get('zendesk','user'), cfg.get('zendesk','pwd')))
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
                "PWD={};".format(cfg.get('database','native_client'),cfg.get('database','sql_server')
                                 ,cfg.get('database','database'),cfg.get('database','data_uid')
                                 ,cfg.get('database','data_pwd')))
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


