import json
import methods
import os
import json
import math
import threading
from concurrent.futures import ProcessPoolExecutor
import init
import asyncio
import logging
#root path for all assets and data
#should be htdocs  root for production deployment
path = "/home/wwwroot/tulpa" 
public_htpath = "/home/wwwroot/tulpa"
special_auth_pass = "/home/wwwroot/"
#dictionary for site
logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)
#connection object
p = ProcessPoolExecutor(3) 
#Search Method hash table
def mainList(parsed_json):
    conn_mem = init.init()
        #site dictionary
    site_dict = {}
    #concatenate sql for query hmc
    query_sql_hmc = methods.concatenate_sql().query_main_List(int(parsed_json['page']))
    #concatenate sql for query main_hmc total row for pagination
    query_sql_hmc_trow = methods.concatenate_sql().get_total_row("main_HMC")
    total_row = methods.Database_operation(query_sql_hmc_trow, conn_mem,1).conn()
    #concatenate sql for query tulpa
    #query hmc
    dat_hmc = methods.Database_operation(query_sql_hmc, conn_mem,1).conn()
    page_num = (total_row[0][0]/4)
    logging.debug(str(methods.datetimenow())+"mainList total page number is: " + str(page_num))
    page_num = math.ceil(page_num)
    #print (total_row)
    list_of_site = []
    #if page_num <= parsed_json['page']:
    #    return_json = """{
    #        "error":"Page number out of range"
    #    }"""
    #    return return_json
    #else:
    #    pass
    #print (dat_hmc)
    #Create Site list by looping through hmc query and tulpas query
    for details in dat_hmc:
        site_dict["h_name"] = details[2]
        site_dict["createdDate"] = str(details[1])
        sql_asset = methods.concatenate_sql().query_file(str(details[3]), "webinput")
        print(sql_asset)
        query_asset = methods.Database_operation(sql_asset, conn_mem, 1).conn()
        #print(query_asset)
        site_dict["url"] = str(details[0]) +"/"+query_asset[0][0]
        query_tulpa = methods.concatenate_sql().query_tulpa_main_List(details[3])
        dat_tulpa = methods.Database_operation(query_tulpa, conn_mem, 1).conn()
        list_tulpa = []
        for tulpas in dat_tulpa:
            list_tulpa.append(tulpas[0])
        site_dict["tulpas"] = list_tulpa
        list_of_site.append(site_dict)
        site_dict = {}

    #construct_return dict to be returned and serializedd
    # print(list_of_site)
    return_dict = {
        "request" : "mainList",
        "pagesQuantity": page_num,
        "sites": list_of_site
    }
    conn_mem.close()
    #serialize return_dict to json
    data = json.dumps(return_dict, indent=4)
    return (data)

def uploading(parsed_json):
    conn_mem = init.init()
        #generate file names and path
    h_path = methods.gen_file_name(parsed_json, 2).fname()
    f_name = methods.gen_file_name(parsed_json, 1).fname()
    c_name = methods.gen_file_name(parsed_json, 3).fname()
    host_path = (path+"/"+ h_path)
    #create host path
    os.mkdir(host_path)
    #concatenate sql for db operation
    sql_hmc = methods.concatenate_sql().insert_HMC(parsed_json, host_path)
    query_hmc = methods.Database_operation(sql_hmc, conn_mem, 2).conn()
    #print(type(query_hmc))
    #spawn child process for querying cover
    h_name = str(parsed_json["host_name"])
    print (h_name)
    query_hmc_sql = methods.concatenate_sql.get_host_id(h_name)
    print (query_hmc_sql)
    query_hmc = methods.Database_operation(query_hmc_sql, conn_mem, 1).connect()
    query_hmc_cover = threading.Thread(target=methods.cover_database, args=(c_name,query_hmc,conn_mem,))
    query_hmc_cover.start()
    #loop through tulpa list from json and perform Database INSERTs, spawning child process to speed up
    threads = []
    for i in range(len(parsed_json['tulpas_name'])):
        threads.append(threading.Thread(target=methods.uploading_tulpa, args=(i, parsed_json, query_hmc, conn_mem,)))
        threads[-1].start()
    print (threads)
    for thread in threads:
            thread.join()
    #Writing webinput to asset
    sql_hmc_webinput = threading.Thread(target=methods.uploading_webinput, args=(f_name,query_hmc,conn_mem))
    sql_hmc_webinput.start()
    # print(query_webinput)
    webinput_file = open(host_path+"/"+ f_name+".html", 'w' )
    webinput_file.write(parsed_json['webInput'])
    #write image to file
    #if the image is more than 10MB then return error
    for ind_img in parsed_json["imgs"]:
        if len(ind_img) >= 10000000:
            return ("""{
                "request" : "uploading",
                "error" : "Image File too large"
            }""")
    
    #loop through images for writing
    threads = []
    for i in range(len(parsed_json["imgs"])):
        threads.append(threading.Thread(target= methods.writing_image, args=(host_path,parsed_json,i)))
        threads[-1].start()
    for thread in threads:
        thread.join()
    #decode base64 and write to folders
    
    cover_thread = threading.Thread(target=methods.writing_cover, args=(host_path,parsed_json, c_name,))
    cover_thread.start()
    #wait for the subprocesses to complete
    #query_hmc_cover.join()
    #sql_hmc_webinput.join()
    #cover_thread.join()
    print("Record for host {} have been created with a host id of {}".format(parsed_json["host_name"],query_hmc))

    return_dict = {
        "request" : "uploading",
        "success" : "True"
}
    
    # except:
    #       return_dict = {
    #           "success" : "False"
    #       }
    return_json = json.dumps(return_dict, indent=4)
    conn_mem.close()
    return (return_json)
def admin_list(parsed_json):
    conn_mem = init.init()
    #site dictionary
    site_dict = {}
    #concatenate sql for query hmc
    query_sql_hmc = methods.concatenate_sql().query_main_List(int(parsed_json['page']))
    #concatenate sql for query main_hmc total row for pagination
    query_sql_hmc_trow = methods.concatenate_sql().get_total_row("main_HMC")
    total_row = methods.Database_operation(query_sql_hmc_trow, conn_mem,1).conn()
    #concatenate sql for query tulpa
    #query hmc
    dat_hmc = methods.Database_operation(query_sql_hmc, conn_mem,1).conn()
    page_num = (total_row[0][0]/4)
    logging.debug(str(methods.datetimenow())+"mainList total page number is: "+ str(page_num))
    page_num = math.ceil(page_num)
    #print (total_row)
    list_of_site = []
    #Create Site list by looping through hmc query and tulpas query
    for details in dat_hmc:
        site_dict["h_name"] = details[1]
        site_dict["h_age"] = str(details[2])
        site_dict["id"] = details[0]
        site_dict["created_date"] = str(details[6])
        site_dict["h_email"] = str(details[3])
        if details[5] == 0:
            v_status = False
        if details[5] == 1:
            v_status = True
        site_dict["v_status"] = v_status
        sql_asset = methods.concatenate_sql().query_file(str(details[3]), "webinput")
        print(sql_asset)
        query_asset = methods.Database_operation(sql_asset, conn_mem, 1).conn()
        #print(query_asset)
        site_dict["url"] = str(details[0]) +"/"+query_asset[0][0]
        query_tulpa = methods.concatenate_sql().query_tulpa_main_List(details[3])
        dat_tulpa = methods.Database_operation(query_tulpa, conn_mem, 1).conn()
        list_tulpa = []
        for tulpas in dat_tulpa:
            list_tulpa.append(tulpas[0])
        site_dict["tulpas"] = list_tulpa
        list_of_site.append(site_dict)
        site_dict = {}

    #construct_return dict to be returned and serializedd
    # print(list_of_site)
    return_dict = {
        "request" : "adminList",
        "pagesQuantity": page_num,
        "sites": list_of_site
    }
    conn_mem.close()
    #serialize return_dict to json
    data = json.dumps(return_dict, indent=4)
    return (data)

def adminAuthentication(parsed_json):
    conn_mem = init.init()
    compare_hash = methods.admin.admin_authentication(str(parsed_json["password"]), str(parsed_json["userName"]))
    print(compare_hash)
    if compare_hash == True:
        token =  methods.admin.admin_gen_token()   
        token_sql = methods.concatenate_sql.token_operation(token, 1)    
        methods.Database_operation(token_sql, conn_mem, 2)
        return_dict = {
            "request" : "adminAuthentication",
            "Success" :  True,
            "token": token
        }
        return_json = json.dumps(return_dict, indent=4)
        logging.info(methods.datetimenow()+"User with username"+str(parsed_json["userName"])+"Obtained token")
        logging.debug(methods.datetimenow()+" Function adminAuthentication returned"+return_json)
        return return_json
    else:
        return_dict= {
            "request" : "adminAuthentication",
            "Success" :  False
        }
        return_json = json.dump(return_dict, indent=4)
        return return_json
#Parsing and deserializing
async def parse_all(data):

    loop = asyncio.get_event_loop()

    parsed_json = json.loads(data)
    #mainList method
    if parsed_json['request'] ==  "mainList":
        return mainList(parsed_json)
    #handle uploading request
    elif parsed_json['request'] == "uploading":
        return uploading(parsed_json)
    elif parsed_json['request'] == "adminAuthentaication":
        return adminAuthentication(parsed_json)
    elif parsed_json['request'] == "adminList":
        return admin_list(parsed_json)
        