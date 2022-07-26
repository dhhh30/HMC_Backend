import json
import methods
import os
import base64
import json
#Hash table

#Search Method hash table

#Parsing and deserializing
def parse_all(data, conn_mem):
    parsed_json = json.loads(data)
    #mainList method
    if parsed_json['request'] ==  "mainList":
        query_sql = methods.concatenate_sql().query_HMC(int(parsed_json['page']))
        data = methods.MemDatabase(query_sql, 1)
        return (data)
    #pushNewDoc method
    elif parsed_json['request'] == "pushNewDoc":
        return_to_serialize = {"flag": True}
        #serialize dict into json
        json_ = json.dumps(return_to_serialize, indent=4)
        return(str(json_))
    #delDoc method
    elif parsed_json['request'] == "delDoc":
        return("deldoc")
        pass
    else:
        pass