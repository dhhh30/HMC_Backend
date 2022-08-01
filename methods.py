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
    def __init__(self, sql, conn_obj, op_type):
        self.sql = sql
        self.conn_obj = conn_obj
        self.op_type = op_type
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
        elif op_type ==2:
            conn.execute(sql)
            conn.commit()
            #returns last row id on insert
            return cursor.lastrowid
    def conn(self):
        result = self.connect()
        return result
#concatenate sql statement
class concatenate_sql:
    def __init__(self):
        pass
        # self.parsed_dict = parsed_dict
    #concatenate sql for inserting into HMC
    def insert_HMC(self, parsed_dict):
        sql = ("""INSERT INTO main_HMC (h_name, desc, path, v_status) VALUES ({},{},{},{})
        """.format(parsed_dict['h_name'], parsed_dict['description'], parsed_dict['path'], parsed_dict['v_status']))
        return (sql)
    #concatenate sql for querying main HMC
    def query_HMC(self, pg_num):
        if pg_num == 0:
            strt_num = pg_num+1
            end_num = pg_num+10
        else: 
            strt_num = pg_num*10
            end_num = strt_num+10
        sql = ("""SELECT * FROM main_HMC WHERE id BETWEEN {} AND {}""".format(strt_num, end_num))
        return (sql)
    #concatenate sql for inserting into tulpa
    def insert_tulpa(self, t_name, hID):
        sql = ("""INSERT INTO tulpas (tulpaName, hID) VALUES ({},{})""".format(t_name, hID))
        return (sql)
    #concatenate sql for querying tulpa
    def query_tulpa(self, hID):
        sql = ("""SELECT * FROM tulpas WHERE hID={}""".format(hID))
        return(sql) 
    def insert_doc(self, parsed_json, path):
        pass

   # def get_row_num:
#generate file name
class gen_file_name:
    def __init__(self, parsed_json, op_num):
        ms = int(round(time.time() * 1000))
        rand_num = randrange(10)
        if op_num == 1:
            final_file = (parsed_json["file_name"],"-"+str(ms)+str(rand_num))
            return final_file
        if op_num == 2:
            final_file = (str(ms)+str(rand_num))
            return final_file
        if op_num ==3:
            final_file = (parsed_json["cover_name"],"-"+str(ms)+str(rand_num))
            return final_file