import time
from random import randrange
import base64
import os
import threading
import hashlib, secrets
from init import init
from datetime import datetime
#max concurrent thread
sema = threading.Semaphore(value=16)
#logging time function
def datetimenow():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return str("["+dt_string+"]")

#class for operating with DB
class Database_operation():
    def __init__(self):
        pass
    #connect database for operation
    def connect(sql, conn, op_type):   
        #Cursor for above apsw connection object
        cursor = conn.cursor()
        cursor.execute(sql)
        #op_type 1 = select
        #op_type 2 = insert
        if op_type == 1:
            data = cursor.fetchall()
            #returns fetched data in list
            cursor.close()
            return data
        elif op_type == 2:
            #returns last row id on insert
            conn.commit()
            cursor.close()
            return
#SQL concaatenation
class concatenate_sql:
    def __init__(self):
        pass
        # self.parsed_dict = parsed_dict
    #concatenate sql for inserting into HMC
    def insert_HMC(self, parsed_dict, host_path):
        sql = ("""INSERT INTO main_HMC (id, h_name, h_age, email, description, path, v_status, creation_time)
         VALUES (NULL, "{}","{}","{}","{}","{}","0",NULL)
         """.format(parsed_dict['host_name'], parsed_dict['host_age'], parsed_dict['email'], parsed_dict['introduce'], host_path , 0))
        return (sql)
    #concatenate sql for querying main HMC
    def query_main_List(self, pg_num):
        if pg_num == 1:
            row_num = pg_num-1
        else:
            pg_num -= 1
            row_num = pg_num*10
        sql = ("""SELECT path, creation_time, h_name, id FROM main_HMC LIMIT {}, 4;""".format(row_num))
        print(sql)
        return (sql)
    #concatenate sql for inserting into tulpa
    def insert_tulpa(self,i,  t_name, hID):
        sql = ("""INSERT INTO tulpas (id, tulpaName, hID) VALUES (NULL, "{}",{})""".format(t_name['tulpas_name'][i], hID[0]))
        return (sql)
    #concatenate sql for querying tulpa
    def query_tulpa_main_List(self, hID):
        sql = ("""SELECT tulpaName FROM tulpas WHERE hID={}""".format(hID[0]))
        return(sql) 
    def insert_doc(self, type , path, hID):
        sql = ("""INSERT INTO assets (id, assetPath, type, hID) VALUES (NULL,"{}","{}",{})""".format(path, type, hID[0]))
        return sql
    #get total amount of row from table for pagination
    def get_total_row(self, table):
        sql = ("""SELECT COUNT(*) FROM {}""".format(table))
        return (sql)
    #concatenate sql query for inserting files into database
    def query_file(self, hID, type):
        sql = ("""SELECT assetPath FROM assets WHERE hID='{}' AND type='{}'""".format(hID[0],type))
        return sql
    def query_approve_hmc(self, hID):
        sql = ("""UPDATE * FROM main_HMC WHERE id='{}'""".format(hID[0]))
        return (sql)
    def get_host_id(h_name):
        sql =  """SELECT LAST_INSERT_ID() FROM main_HMC;""".format(h_name)
        return sql
    
    def query_admin_list(self, pg_num, v_status):
        if pg_num == 1:
            row_num = pg_num-1
        else:
            pg_num -= 1
            row_num = pg_num*10
        
        if v_status != "":
            if v_status == True:
                v_status = 1
            if v_status == False:
                v_status = 0
            sql = ("""SELECT * FROM main_HMC WHERE v_status='{}' LIMIT {}, 4;""".format(str(v_status), row_num))
        else:
            sql = ("""SELECT * FROM mainHMC LIMIT {}, 4""".format(row_num))

        return (sql)
    def token_operation(token, op_code):
        #if the operation is to insert token into admin_token
        if op_code == 1:
            sql = ("""INSERT INTO admin_token (token, issued_time) VALUES('{}', NULL)""".format(token))
        #if the operation is to query token from admin_token
        if op_code == 2:
            sql = ("""SELECT token FROM admin_token WHERE token = '{}'""".format(token))
        if op_code == 3:
            sql = ("""SELECT EXISTS(SELECT * from admin_token WHERE token = '{}')""".format(token))
        return sql
    