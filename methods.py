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
sema = threading.Semaphore(value=8)

#class for operating with DB
class Database_operation():
    def __init__(self, sql, conn_obj, op_type, table):
        self.sql = sql
        self.conn_obj = conn_obj
        self.op_type = op_type
        self.table = table
        
    def connect(self):   
        #Sql Statement
        sql = self.sql
        #Operation Type
        op_type = self.op_type
        #Connection object for both memDB and HDDB
        conn = self.conn_obj
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
            conn.commit()
            cursor.execute(' SELECT MAX(id) FROM {};'.format(self.table))
            #returns last row id on insert
            last_id =  cursor.fetchone()
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
         """.format(parsed_dict['host_name'], parsed_dict['host_age'], parsed_dict['email'], parsed_dict['introduce'], host_path , 0))
        return (sql)
    #concatenate sql for querying main HMC
    def query_main_List(self, pg_num):
        if pg_num != 0: 
            pg_num = pg_num*10
        sql = ("""SELECT path, creation_time, h_name, id FROM main_HMC LIMIT {}, 10""".format(pg_num))
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
    def get_total_row(self, table):
        sql = ("""SELECT COUNT(*) FROM {}""".format(table))
        return (sql)
    def query_file(self, hID, type):
        sql = ("""SELECT assetPath FROM assets WHERE hID='{}' AND type='{}'""".format(hID[0],type))
        return sql
   # def get_row_num:
#generate file name
class gen_file_name:
    def __init__(self, parsed_json, op_num):
        self.parsed_json = parsed_json
        self.op_num = op_num
    def fname(self):
        ms = int(round(time.time() * 1000))
        rand_num = randrange(10)
        if self.op_num == 1:
            final_file = (str(ms)+str(rand_num))
            return final_file
        if self.op_num == 2:
            final_file = (str(self.parsed_json["host_name"])+"-"+str(ms)+str(rand_num))
            return final_file
        if self.op_num ==3:
            final_file = (str(self.parsed_json["cover_name"])+"-"+str(ms)+str(rand_num))
            return final_file

def cover_database(c_name, query_hmc, conn_mem):
    sema.acquire()
    #sql for INSERTING into assets for HMC cover
    sql_hmc_cover = concatenate_sql().insert_doc("cover", c_name, query_hmc)
    #query for executing code for hmc cover
    Database_operation(sql_hmc_cover,conn_mem, 2, "assets").conn()
    sema.release()
def uploading_tulpa(i, parsed_json, query_hmc, conn_mem):
    sema.acquire()
    sql_tulpa = concatenate_sql().insert_tulpa(i, parsed_json, query_hmc)
    print(sql_tulpa)
    Database_operation(sql_tulpa, conn_mem, 2, "tulpas").conn()
    sema.release()
def uploading_webinput(f_name, query_hmc, conn_mem):
    sema.acquire()
    #concatenate sql for storing webinput records in asset table
    sql_hmc_webinput = concatenate_sql().insert_doc("webinput", f_name+".html", query_hmc)
    Database_operation(sql_hmc_webinput, conn_mem, 2, "assets").conn()
    sema.release()
def writing_image(host_path, parsed_json, i):
    sema.acquire()
    #decoding image from base64 and write them into perspective files
    image_file = open(os.path.join(host_path, parsed_json["img_names"][i]), 'wb')
    image_file.write(base64.b64decode(parsed_json["imgs"][i]))
    image_file.close()
    sema.release()
def writing_cover(host_path, parsed_json):
    sema.acquire()
    cover_file = open(os.path.join(host_path, parsed_json["cover_name"]), 'wb')
    cover_file.write(base64.b64decode(parsed_json["cover"]))
    cover_file.close()
    sema.release()
