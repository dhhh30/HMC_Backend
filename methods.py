from select import select
from os import path
from unittest import result
from mysql import connector
import time
from random import randrange


#Abstract Database Object
class AbstractDatabase:
    def __init__(self):
        pass


#class for operating with HDDB
#class for operating with MEMDB
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
            return data
        elif op_type == 2:
            conn.commit()
            cursor.execute(' SELECT MAX(id) FROM {};'.format(self.table))
            #returns last row id on insert
            return cursor.fetchone()
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
            final_file = (self.parsed_json["file_name"]+"-"+str(ms)+str(rand_num))
            return final_file
        if self.op_num == 2:
            final_file = (self.parsed_json["host_name"]+"-"+str(ms)+str(rand_num))
            return final_file
        if self.op_num ==3:
            final_file = (self.parsed_json["cover_name"]+"-"+str(ms)+str(rand_num))
            return final_file