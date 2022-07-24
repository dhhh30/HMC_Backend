import json
import methods
import sqlite3
#Hash table

#Search Method hash table

#Initial Parsing
#def load_db_ram():
#    hdd = sqlite3.connect()

def parse_all(data):
    parsed_json = json.loads(data)
    #mainList method
    if parsed_json['request'] ==  "mainList":
        query_sql = methods.concatenate_sql().query_HMC(int(parsed_json['page']))
        data = methods.MemDatabase(query_sql, 1)
        return (data)
        return ('123')
    #pushNewDoc method
    elif parsed_json['request'] == "pushNewDoc":

        return("pushnewdoc")
        pass
    #deldoc
    elif parsed_json['request'] == "delDoc":
        return("deldoc")
        pass
    else:
        pass