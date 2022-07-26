from select import select
import sqlite3
from os import path
from unittest import result
import apsw

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
    def insert_HMC(self, parsed_dict):
        sql = ("""INSERT INTO MainHMC (h_name, desc, path, v_status) VALUES ({},{},{},{})
        """.format(parsed_dict['h_name'], parsed_dict['description'], parsed_dict['path'], parsed_dict['v_status']))
        return (sql)
    def query_HMC(self, pg_num):
        if pg_num == 0:
            strt_num = pg_num+1
            end_num = pg_num+10
        else: 
            strt_num = pg_num*10
            end_num = strt_num+10
        sql = ("""SELECT * FROM MainHMC WHERE hostID BETWEEN {} AND {}""".format(strt_num, end_num))
        return (sql)
        
    def insert_tulpa():
        
        pass
    def query_tulpa(self, tID):
        sql = select
        pass
    def insert_doc(self, dict, path):
        pass