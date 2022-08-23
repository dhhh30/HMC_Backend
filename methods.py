from select import select
from os import path
from unittest import result
from mysql import connector
import time
from random import randrange
import base64
import os
import sys
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
    return ("["+dt_string+"]")
#class for operating with DB
class Database_operation():
    def __init__(self, sql, conn_obj, op_type):
        self.sql = sql
        self.conn_obj = conn_obj
        self.op_type = op_type
    
    #connect database for operation
    def connect(self):   
        #Sql Statement
        sql = self.sql
        #Operation Type
        op_type = self.op_type
        #Connection object for both memDB and HDDB
        conn = self.conn_obj
        #Cursor for above apsw connection object
        cursor = conn.cursor(multi=True)
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
            last_id =  cursor.fetchone()
            conn.commit()
            cursor.close()
            return last_id
    def conn(self):
        result = self.connect()
        return result
#concatenate sql statement
class concatenate_sql:
    def __init__(self):
        pass
        # self.parsed_dict = parsed_dict
    #concatenate sql for inserting into HMC
    def insert_HMC(self, parsed_dict, host_path):
        sql = ("""INSERT INTO main_HMC (id, h_name, h_age, email, description, path, v_status, creation_time)
         VALUES (NULL, "{}","{}","{}","{}","{}","0",NULL);
         SELECT LAST_INSERT_ID()
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
        sql = ("""SELECT tulpaName FROM tulpas WHERE hID={}""".format(hID))
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
        sql = ("""UPDATE * FROM Main_HMC WHERE hID='{}'""".format(hID))
        return (sql)
    def get_last_id(table):
        sql =  """SELECT hID from {} ORDER BY hID DESC LIMIT 1;""".format(table)
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
    
    
#generate file name
class gen_file_name:
    def __init__(self, parsed_json, op_num):
        self.parsed_json = parsed_json
        self.op_num = op_num
    #generate file name
    def fname(self):
        ms = int(round(time.time() * 1000))
        rand_num = randrange(10)
        #generate file name
        if self.op_num == 1:
            final_file = (str(ms)+str(rand_num))
            return final_file
        #generate folder name
        if self.op_num == 2:
            final_file = (str(self.parsed_json["host_name"])+"-"+str(ms)+str(rand_num))
            return final_file
        #generate jpg
        if self.op_num ==3:
            final_file = (str("cover")+"-"+str(ms)+str(rand_num)+".jpg")
            return final_file

def cover_database(c_name, query_hmc, conn_mem):
    sema.acquire()
    #sql for INSERTING into assets for HMC cover
    sql_hmc_cover = concatenate_sql().insert_doc("cover", c_name, query_hmc)
    #query for executing code for hmc cover
    Database_operation(sql_hmc_cover,conn_mem, 2, "assets").conn()
    sema.release()
    return
def uploading_tulpa(i, parsed_json, query_hmc, conn_mem):
    sema.acquire()
    sql_tulpa = concatenate_sql().insert_tulpa(i, parsed_json, query_hmc)
    print(sql_tulpa)
    Database_operation(sql_tulpa, conn_mem, 2, "tulpas").conn()
    sema.release()
    return
def uploading_webinput(f_name, query_hmc, conn_mem):
    sema.acquire()
    #concatenate sql for storing webinput records in asset table
    sql_hmc_webinput = concatenate_sql().insert_doc("webinput", f_name+".html", query_hmc)
    Database_operation(sql_hmc_webinput, conn_mem, 2, "assets").conn()
    sema.release()
    return
def writing_image(host_path, parsed_json, i):
    sema.acquire()
    #decoding image from base64 and write them into perspective files
    image_file = open(os.path.join(host_path, str(parsed_json["imgs_names"])[i]), 'wb')
    image_file.write(base64.b64decode(str(parsed_json["imgs"][i])))
    image_file.close()
    sema.release()
    return
#write cover to disk
def writing_cover(host_path, parsed_json, cover_name):
    sema.acquire()
    cover_file = open(os.path.join(host_path, cover_name), 'wb')
    cover_file.write(base64.b64decode(parsed_json["cover"]))
    cover_file.close()
    sema.release()
    return
class admin():
    def __init__(self):
        pass
    def admin_authentication(pwd, uname):
        conn = init()
        #Detect if uname = email
        if "@" in uname == True:
            sql = """SELECT pwd_hash FROM admin_usr WHERE {} = '{}'""".format("email",uname)
        else:
            sql = """SELECT pwd_hash FROM admin_usr WHERE {} = '{}'""".format("uname",uname)
        #hash the input plain text pwd
        input_hash = hashlib.sha256(bytes(pwd)).digest()
        #query hashed pwd from database
        output_hash = bytes(Database_operation(sql, conn, 1).connect())
        #compare hashes
        return secrets.compare_digest(input_hash, output_hash)
    def admin_gen_token():
        #random sha256 generation function
        ms = int(round(time.time() * 1000))
        rand_num = randrange(100)
        token = hashlib.sha256(bytes(str(ms), "utf-8")).digest()
        token = hashlib.sha256(bytes(str(token)+str(rand_num) , "utf-8"))
        #encode sha256 into base64
        token = base64.encodebytes(token)
        return token
            
    def admin_token_auth(token):
        token = str(Database_operation(str(concatenate_sql.token_operation(token)), init(), 1).connect())
        
        pass
