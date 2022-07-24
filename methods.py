import sqlite3
from os import path
from unittest import result
import sqlalchemy.pool


class AbstractDatabase:
    def __init__(self):
        pass
        
    def connect(self, conn_name, sql, op_type):
        sqlite = sqlalchemy.pool.manage(sqlite3, poolclass=sqlalchemy.pool.SingletonThreadPool)
        self.conn_name = conn_name
        self.sql = sql
        self.op_type = op_type
        self.conn = sqlite.connect(self.conn_name)
        cursor = self.conn.cursor()
        print(sql)
        self.conn.cursor().execute(str(self.sql))
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
        result = super().connect("database.db", sql, op_type)
#class for operating with MEMDB
class MemDatabase(AbstractDatabase):
    def __init__(self, sql, op_type):
        result = super().connect("file::memory:?cache=shared", sql, op_type)
        HD_result = HDDatabase().operate(sql, op_type)
        return result
#concatenate sql statement
class concatenate_sql:
    def __init__(self):
        pass
        # self.parsed_dict = parsed_dict
    def insert_HMC():

        pass
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
    def query_tulpa():
        pass
