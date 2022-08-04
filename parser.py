import hashlib
import json
import methods
import os
import base64
import json
import math
#root path for all assets and data
#should be in htdocs for production deployment
path = "/Users/yurunchen/Documents/GitHub/HMC_backend/" 

#dictionary for site

#Hash table

#Search Method hash table

#Parsing and deserializing
def parse_all(data, conn_mem):
    parsed_json = json.loads(data)
    #mainList method
    if parsed_json['request'] ==  "mainList":
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

        page_num = (total_row[0][0]/10)
        page_num = math.ceil(page_num)
       #print (total_row)
        list_of_site = []
        
        #print (dat_hmc)
        for details in dat_hmc:
            site_dict["url"]= details[0]
            site_dict["h_name"] = details[2]
            site_dict["createdDate"] = str(details[1])
            query_tulpa = methods.concatenate_sql().query_tulpa_main_List(details[3])
            dat_tulpa = methods.Database_operation(query_tulpa, conn_mem, 1).conn()
            list_tulpa = []
            for tulpas in dat_tulpa:
                list_tulpa.append(tulpas[0])
            site_dict["tulpas"] = list_tulpa
            list_of_site.append(site_dict)
            site_dict = {}
        #construct_return dict to be returned and serializedd
        return_dict = {
            "pagesQuantity": page_num,
            "sites": list_of_site
        }

        #serialize return_dict to json
        data = json.dumps(return_dict, indent=4)
        return (data)
    #handle uploading request
    elif parsed_json['request'] == "uploading":
        #generate file names and path
        h_path = methods.gen_file_name(parsed_json, 2).fname()
        f_name = methods.gen_file_name(parsed_json, 1).fname()
        c_name = methods.gen_file_name(parsed_json, 3).fname()
        host_path = os.path.join(path, h_path)
        # try:
        #create host path
        os.mkdir(host_path)
        #concatenate sql for db operation
        sql_hmc = methods.concatenate_sql().insert_HMC(parsed_json, host_path)
        query_hmc = methods.Database_operation(sql_hmc, conn_mem, 2, "main_HMC").conn()
        #print(type(query_hmc))
        if parsed_json['file'] == None:
            pass   
        else:
            sql_hmc_file = methods.concatenate_sql().insert_doc("file", f_name, query_hmc)
            sql_hmc_cover = methods.concatenate_sql().insert_doc("cover", c_name, query_hmc)
        #print(sql_hmc_file)
        query_hmc_file = methods.Database_operation(sql_hmc_file,conn_mem, 2, "assets").conn()
        query_file_cover = methods.Database_operation(sql_hmc_cover,conn_mem, 2, "assets").conn()
        for i in range(len(parsed_json['tulpas_name'])):
            
            sql_tulpa = methods.concatenate_sql().insert_tulpa(i, parsed_json, query_hmc)
            print(sql_tulpa)
            query_tulpa = methods.Database_operation(sql_tulpa, conn_mem, 2, "tulpas").conn()
        print (sql_hmc_file, sql_hmc_cover)
        
        sql_hmc_webinput = methods.concatenate_sql().insert_doc("webinput", os.path.join(host_path, f_name)+"html", query_hmc)
        query_webinput = methods.Database_operation(sql_hmc_webinput, conn_mem, 2, "assets")
        webinput_file = open(os.path.join(host_path, f_name)+".html", 'w' )
        webinput_file.write(parsed_json['webinput'])
        #decode base64 and write to folders
        cover_file = open(os.path.join(host_path, parsed_json["cover_name"]), 'wb')
        cover_file.write(base64.b64decode(parsed_json["cover"]))
        cover_file.close()

        file_file = open(os.path.join(host_path, parsed_json["file_name"]), 'wb')
        file_file.write((base64.b64decode(parsed_json["file"])))
        file_file.close()
        return_dict = {
            "success" : "True"
        }
        # except:
        #     return_dict = {
        #         "success" : "False"
        #     }
        return_json = json.dumps(return_dict, indent=4)
        return (return_json)
        
        
    # #pushNewDoc method
    # elif parsed_json['request'] == "pushNewDoc":
    #     return_to_serialize = {"flag": True}
    #     #serialize dict into json
    #     json_ = json.dumps(return_to_serialize, indent=4)
    #     return(str(json_))
    # #delDoc method
    # elif parsed_json['request'] == "delDoc":
    #     return("deldoc")
    #     pass
    # else:
    #     pass