#rbac automaion snowflake script using xlsx file

import pandas as pd
dct = pd.read_excel("C:\\Downloads\\RBAC Automation Excel sheet.xlsx",sheet_name="Sheet2")

col = dct.columns

def grantDB(privilage,db_name,role):
    query = "grant {} on database {} to role {}".format(privilage,db_name,role)
    print(query)
    print("0")

# condition futureflag == True and allflag == True never comes according to docs
# f = 1 a = 0
# f = 0 a = 1
# f = 0 a = 0
#

def grantSchema(privilage,role,schema_name):
    query = "grant {} on schema {} to role {}".format(privilage,schema_name,role)
    print(query)
    print("1")

def grantfutureschema(privilage,db_name,role):
    query = "GRANT {} ON FUTURE SCHEMAS IN DATABASE {} to role {}".format(privilage,db_name,role)
    print(query)
    print("2")

def grantallschema(privilage,db_name,role):
    query = "GRANT {} ON ALL SCHEMAS IN DATABASE {} to role {}".format(privilage,db_name,role) 
    print(query)
    print("3")

def granttable(privilage,role,schema_name="",table_name="",allflag=False,futureflag=False):
    query = "grant {} on table {} to role {}".format(privilage,table_name,role)
    print(query)
    print("4")

def grantfuturetable(privilage,schema_name,role):
    query = "GRANT {} ON FUTURE TABLES IN SCHEMA {} to role {}".format(privilage,schema_name,role)
    print(query)
    print("5")

def grantalltable(privilage,schema_name,role):
    query = "GRANT {} ON ALL TABLES IN SCHEMA {} to role {}".format(privilage,schema_name,role) 
    print(query)
    print("6")

def grantwarehouse(privilage,warehouse_name,role):
    query = "grant {} on warehouse {} to role {}".format(privilage,warehouse_name,role)
    print(query)
    print("7")

print(dct)

for i in range(0,len(dct["Sr No"])):

    privilage = dct["Privilages"][i]
    
    database = dct["Database"][i]
    schema = dct["Schema"][i]
    table = dct["Table"][i]

    warehouse = dct["Warehouse"][i]
    role = dct["Role"][i]

    if type(dct["Database"][i]) == str and type(dct["Schema"][i]) == str and type(dct["Table"][i]) == str:
        obj_type = "table"
    elif type(dct["Database"][i]) == str and type(dct["Schema"][i]) == str and type(dct["Future"][i]) == str:
        obj_type = "table"
    elif type(dct["Database"][i]) == str and type(dct["Schema"][i]) == str:
        obj_type ="schema"
    elif type(dct["Database"][i]) == str and type(dct["Future"][i]) == str:
        obj_type = "schema"
    elif type(dct["Database"][i]) == str and type(dct["Schema"][i]) == float and type(dct["Table"][i]) == float :
        obj_type = "database"
    else:
        obj_type = "warehouse"


    if obj_type == "table" :
        if (type(dct["Future"][i]) == float) & (dct["Table"] [i] != "all"):
            grantDB("usage",dct["Database"][i],dct["Role"][i])
            grantSchema(privilage="usage",schema_name=database+"."+schema,role= role)
            granttable(privilage=privilage,table_name=database+"."+schema+"."+table, role=role)

        elif type(dct["Future"][i]) == str:
            grantfuturetable(privilage=privilage,schema_name= database+"."+schema, role=role)

        else:
            grantalltable(privilage=privilage,schema_name=database+"."+schema, role=role)

    elif obj_type == "schema":
        if (type(dct["Future"][i]) == float) & (dct["Schema"][i] != "all"):
            grantDB("usage",dct["Database"][i],dct["Role"][i])
            grantSchema(privilage=privilage,schema_name=database+"."+schema,role= role)
        
        elif type(dct["Future"][i]) == str:
            grantfutureschema(privilage=privilage,db_name=database,role=role)

        else:
            grantallschema(privilage=privilage,db_name=database,role=role)
        
    elif obj_type == "database":
        pass
    else:
        grantwarehouse(privilage=privilage,warehouse_name= warehouse,role= role)


###################################################################################################################################
###################################################################################################################################

# teradata to snowflake query conversion using selenium web scraping

from threading import Event
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.headless = True

driverservice = Service('C:\\Users\\sumedhnpatil\\Downloads\\chromedriver_win32\\chromedriver.exe')

driver = webdriver.Chrome(service=driverservice, options=options)
driver.get('https://roboquery.com//app')
objlist = Select(driver.find_element_by_id('ObjType'))
convertbutton = driver.find_element(By.ID, "btnconvert")
element = driver.find_element(By.CSS_SELECTOR, "body.mdl-demo.mdl-color--grey-100.mdl-base:nth-child(2) div.mdl-layout.mdl-js-layout.mdl-layout--fixed-header main.mdl-layout__content:nth-child(2) section.section--center.mdl-grid.mdl-grid--no-spacing.mdl-shadow--2dp:nth-child(2) div.mdl-card.mdl-cell.mdl-cell--12-col div.mdl-card__supporting-text div.CodeMirror.cm-s-default:nth-child(2) div.CodeMirror-scroll:nth-child(6) div.CodeMirror-sizer:nth-child(1) div.CodeMirror-lines div:nth-child(1) div.CodeMirror-code:nth-child(5) div:nth-child(1) > pre.CodeMirror-line")
answer = driver.find_element(By.CSS_SELECTOR, "#txtFeedback")

def convert(query: str, objtype: str):

            if objtype == 'table ddl':
                  pass

            if objtype == 'view ddl':
                  objlist.select_by_index(1)  # for view DDL
                  element.click()

            if objtype == 'sql query':
                  objlist.select_by_index(2)  # for sql query
                  element.click()

            
            # query = """CREATE MULTISET TABLE br_jobs ,NO FALLBACK \\
            #       (\\
            #       job_code INTEGER NOT NULL,\\
            #       pay_grade SMALLINT,\\
            #       legacy_flag BYTEINT NOT NULL,\\
            #       job_title VARCHAR(80) CHARACTER SET Latin NOT CaseSpecific NOT NULL)\\
            #       UNIQUE PRIMARY INDEX ( job_code );"""

            var = "editor.setValue('" + query + "');"
            driver.execute_script(var)
            # driver.execute_script("editor.setValue('create multiset table table1 (id int);');")
            convertbutton.click()
            Event().wait(5)
            driver.execute_script("arguments[0].value = editor.getValue()", answer)
            rslt = answer.get_attribute("value")
            print(rslt)

            driver.quit()


######################################################################################################################################
######################################################################################################################################

# pyhton code to transform double header file to single header file using csv library

import csv

filename = "C:\\downloads\\cowin_vaccine_data_districtwise.csv"
mainlst = []
answerlst = []
#  opening csv file

with open(filename, 'r') as csvfile:

    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    header = header[0:2896]
    first6columns = header[1:6]
    columnsremainingafterstate = next(csvreader)
    columnsremainingafterstate = columnsremainingafterstate[6:16]
    mainpurposedate = []
    statelist = []
    columnsremainingafterstate.extend(first6columns)
    columnsremainingafterstate.insert(0, 'Date')

    # loading all rows in mainlst
    for row in csvreader:
        mainlst.append(row[0:2896])

    # loading dates from 0 th row from header in the array of mainpurpose date
    for i in range(6, 2896, 10):
        mainpurposedate.append(header[i])

    # loading state name , distyrict name ... first 5 columns in statelist
    for i in range(0, len(mainlst)):
        statelist.append(mainlst[i][1:6])
               
    #  loading data on each day basis considering column batch of 10
    rowno = 0
    while(rowno < 754):
        for i in range(6, 2896, 10):
            answerlst.append(mainlst[rowno][i:i+10])
        rowno += 1

    # adding date and state name to each row in answerlst
    for i in range(0, len(answerlst)):
        answerlst[i].insert(0, mainpurposedate[i % 289])
        answerlst[i].extend(statelist[i // 289])

#  create new file with final transform result
with open("anslststate.csv", 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(columnsremainingafterstate)
    for ele in answerlst:
        spamwriter.writerow(ele)

####################################################################################################################################
####################################################################################################################################

# python code to download all tables data inside snowflake cloud datawarehouse in csv format on local machine
# prerequisite : Snowflake Account must have running warehouse.

import snowflake.connector
import csv



# function to write all rows from tables in csv file
def downdb(ctx, cs, databaselst : list, downloaddirectory : str):
    def writerow(tablename: str, finalcollst: list, finalrowlst: list):
        with open(downloaddirectory + tablename + ".csv", 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(finalcollst)
            for ele in finalrowlst:
                spamwriter.writerow(ele)

    try:
        '''
        optional warehouse 
        # warehouse = '<specify warehouse name to be used>'

        # role = 'sysadmin'  # '<specify role to be used>'

        # cs.execute("use warehouse "+ warehouse)
        # whrslt = cs.fetchall()

        optional role
        # cs.execute("use role " + role)
        # rolerslt = cs.fetchall()
        # print(rolerslt)

        '''


        # get all schemas names in respective database except INFORMATION_SCHEMA

        schemalst = []
        for db in databaselst:
            cs.execute("show schemas in database " + db)
            schemasindb = cs.fetchall()
            for schema in schemasindb:
                if schema[1] != 'INFORMATION_SCHEMA':
                    schemalst.append(schema[4]+"."+schema[1])

        # get all tables names in respective schemas in respective database

        tableslst = []
        tableslstfile = []
        for schema in schemalst:
            cs.execute("show tables in schema " + schema)
            tablesinschemas = cs.fetchall()
            for table in tablesinschemas:
                tableslst.append("\""+table[2]+"\""+"." +
                             "\""+table[3]+"\""+"."+"\""+table[1]+"\"")
                tableslstfile.append(table[2]+"."+table[3]+"."+table[1])

        # get all rows from all tables in respective schema and respectiv database

        for i in range(0, len(tableslst)):
            cs.execute('desc table ' + tableslst[i])
            columnlst = cs.fetchall()
            finalcollst = []
            for column in columnlst:
                finalcollst.append(column[0])
            cs.execute("select * from " + tableslst[i])
            rowlst2 = cs.fetchall()
            finalrowlst = []
            for row in rowlst2:
                finalrowlst.append(row)
            writerow(tableslstfile[i], finalcollst, finalrowlst)


    finally:
        cs.close
    ctx.close


ctx = snowflake.connector.connect(
    user= '<give username ex : Tom>',
    
    password='<give password or user ex : 1234 >',
    
    account= '<give account url till .snowflakecomputing.com>'
)
cs = ctx.cursor()

databaselst = []
download_directory_name = "c:\\test\\"
downdb(ctx, cs, databaselst, download_directory_name)


##################################################################################################################################
##################################################################################################################################

