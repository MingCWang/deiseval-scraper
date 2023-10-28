'''
Failed attempt to connect to Azure SQL database
'''
import os
import pyodbc, struct
from azure import identity


from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

    
# connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]


def get_conn():
    
    SERVER = 'tcp:myfreedbserver8.database.windows.net' 
    DATABASE = 'myFreeDB' 
    USERNAME = '{Ming-Shih Wang}' 
    PASSWORD = 'mth9dbh@HDY!pwy!mjn' 

    
    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};'
    conn = pyodbc.connect(connectionString) 
    print("Connected to database")
    # credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    # token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    # token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    # SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    # conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})  



get_conn()