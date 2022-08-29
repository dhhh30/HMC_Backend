#Parsing and deserializing
import methods_ohaul as methods
import json
from concurrent.futures import ProcessPoolExecutor
import pdb
import init
import asyncio
# pdb.set_trace()
def parse_all(parsed_json):
    #mainList method
    if parsed_json['request'] == "mainList":
        return methods.general_request.mainList(parsed_json)
    #handle uploading request
    elif parsed_json['request'] == "uploading":
        return methods.general_request.uploading(parsed_json)
    elif parsed_json['request'] == "adminAuthentication":
        conn_mem = init.init()
        compare_hash = methods.admin.admin_authentication(parsed_json["password"] , parsed_json["userName"])
        # print(compare_hash, flush=True)
        if compare_hash == True:
            token =  methods.admin.admin_gen_token()   
            token_sql = methods.sql_operation.token_operation(token, 1)    
            methods.database.connect(token_sql, conn_mem, 2)
            print(token)
            return_dict = {
                "request" : "adminAuthentication",
                "Success" :  "true",
                "token": str(token)
            }
            return_json = json.dumps(return_dict, indent=4)
            return (return_json)
        elif compare_hash == False:
            return_dict= {
                "request" : "adminAuthentication",
                "Success" :  "false"
            }
            return_json = json.dumps(return_dict, indent=4) 
            return (return_json)

    elif parsed_json['request'] == "adminList":
        return methods.admin_request.adminList(parsed_json)
    elif parsed_json['request'] == "audit":
        if parsed_json['audit'] == "pass":
            return methods.admin_request.adminApprove(parsed_json)
        elif parsed_json['audit'] == "reject":
            return methods.admin_request.adminDeny(parsed_json)

    