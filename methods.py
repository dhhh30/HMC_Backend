from select import select
import sqlite3
from os import path
from unittest import result
import apsw
import time
from random import randrange


#Abstract Database Object
class AbstractDatabase:
    def __init__(self):
        pass
    def connect(self, sql, conn_obj, op_type):   
        #Sql Statement
        self.sql = sql
        #Operation Type
        self.op_type = op_type
        #Connection object for both memDB and HDDB
        self.conn = conn_obj
        #Cursor for above apsw connection object
        cursor = self.conn.cursor()
        #op_type 1 = select
        #op_type 2 = insert
        if self.op_type == 1:
            data = cursor.fetchall()
            #returns fetched data in list
            return data
        elif self.op_type ==2:
            self.conn.commit()
            #returns last row id on insert
            return cursor.lastrowid

#class for operating with HDDB
class HDDatabase(AbstractDatabase):
    def operate(self, sql, op_type):
        conn = sqlite3.connect("database.db")
        result = super().connect(sql, conn, op_type)
        return (result)
#class for operating with MEMDB
class MemDatabase(AbstractDatabase):
    def __init__(self, sql, memcon, op_type):
        result = super().connect(":memory:", sql, op_type)
        HD_result = HDDatabase().operate(sql, op_type)
        if result != None:
            return (result)
        else:
            return(False)
#concatenate sql statement
class concatenate_sql:
    def __init__(self):
        pass
        # self.parsed_dict = parsed_dict
    #concatenate sql for inserting into HMC
    def insert_HMC(self, parsed_dict):
        sql = ("""INSERT INTO MainHMC (h_name, desc, path, v_status) VALUES ({},{},{},{})
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
        sql = ("""SELECT * FROM MainHMC WHERE hostID BETWEEN {} AND {}""".format(strt_num, end_num))
        return (sql)
    #concatenate sql for inserting into tulpa
    def insert_tulpa(self, t_name, hID):
        sql = ("""INSERT INTO Tulpas (tulpaName, hID) VALUES ({},{})""".format(t_name, hID))
        return (sql)
    #concatenate sql for querying tulpa
    def query_tulpa(self, hID):
        sql = ("""SELECT * FROM Tulpas WHERE hID={}""".format(hID))
        return(sql) 
    def insert_doc(self, parsed_json, path):
        pass
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