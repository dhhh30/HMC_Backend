#Parsing and deserializing
import methods_ohaul as methods
import json
from concurrent.futures import ProcessPoolExecutor
import pdb

import asyncio

async def parse_all(data):
    parsed_json = json.loads(data)
    #mainList method
    if parsed_json['request'] == "mainList":
        return methods.general_request.mainList(parsed_json)
    #handle uploading request
    elif parsed_json['request'] == "uploading":
        return methods.general_request.uploading(parsed_json)
    elif parsed_json['request'] == "adminAuthentaication":

        response =methods.admin_request.adminAuthentication(parsed_json)
        breakpoint()
        return response
    elif parsed_json['request'] == "adminList":
        return methods.admin_request.adminList(parsed_json)
    # elif parsed_json['request'] == "adminApprove":
    #     return methods.adminApprove(parsed_json)
    # elif parsed_json['request'] == "adminDeny":
    #     return methods.adminDeny(parsed_json)

    