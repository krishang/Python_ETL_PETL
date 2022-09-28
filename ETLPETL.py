# Author : KrishanG
# Date   : 26/09/2022
# Remarks: The following script extracts the csv files located in the said path and loads this into a database. Check the log file ETL_Errors.csv for errors. Note each table name will correspond to the csv file name 
#          Petl uses lazy loading thus the DB field lengths will not be accurate and throw out trunction errors. To figure out which tables and fields cause this, enable the following on the DB for tracing. Do not do this 
#           on a production server. Switch off once the errors have been isolated.
#          /* This script needs to be run on the MSSQL server. At the time of the writing I am using SQL2016. Check equivalent for other versions.
#            Enable and disbale error tracing on the tables 
#            DBCC TRACEON(460, -100);  -- enable errors
#            DBCC TRACEOFF(460, -100); -- disable errors
#            GO
#          */
# download the missing packages using pip note the parameters to get pass the ssl error. this is if you are using somthing like netbox blue, which requires a local certificate.
# pip install --trusted-host=pypi.org --trusted-host=files.pythonhosted.org --user pymssql


import os
import sys
import petl
import pymssql
import configparser
import requests
from datetime import datetime
import json
import decimal
import openpyxl
import pandas as pd
from os import walk




# get data from configuration file
config = configparser.ConfigParser()
try:
    config.read('config.ini')
except Exception as e:
    print('could not read configuration file:' + str(e))
    sys.exit();


    # read settings from configuration file
startDate = config['CONFIG']['startDate']
url = config['CONFIG']['url']
destServer = config['CONFIG']['server']
destDatabase = config['CONFIG']['database']
cUser= config['CONFIG']['User']
cPassword = config['CONFIG']['Password']
sFTPPath=config['CONFIG']['Path']
# print (config)
    

CSV_Files = next(walk(sFTPPath), (None, None, []))[2]  # [] if no file

print (CSV_Files)
tblErrors=  [['Log_date', 'ErrorLine'],]

for file in CSV_Files:
        # load expense document
        FilePath=sFTPPath+file
        try:
            data = petl.io.csv.fromcsv(FilePath)
            print(data)  
            dbConnection = pymssql.connect(server=destServer,user=cUser,password=cPassword, database=destDatabase)
            file=file.replace('.csv','')
            sql="SELECT  count(*) as TableAvailable FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME='"+file +"'" 
           
            IsTable=  petl.io.fromdb(dbConnection,sql)['TableAvailable'][0]
            #print(IsTable)
       
            petl.io.todb (data,dbConnection,file,create= not bool(IsTable))
      
        except Exception as e:
           print('could not open csv:'+ FilePath+' Detail error:' + str(e))
           tblErrors.append([datetime.now()  ,'could not open csv:'+ FilePath+' Detail error:' + str(e)])

print ('***************************************Error Report*******************************************************')          
print (pd.DataFrame(tblErrors))

petl.tocsv(tblErrors,sFTPPath+ 'ETL_Errors.csv')
sys.exit()
    


