import hashlib
import json
import methods
import os
import base64
import json
#root path for all assets and data
path = "/Users/yurunchen/Documents/GitHub/HMC_Backend/"    
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
        query_sql_hmc = methods.concatenate_sql().query_HMC(int(parsed_json['page']))
        #concatenate sql for query tulpa
        
        #query hmc
        dat_hmc = methods.Database_operation(query_sql_hmc, conn_mem,1).conn()
        #query tulpa
        
        list_of_site = []
        #sort the datas and insert into the list_of_site list
        for details in dat_hmc:
            site_dict["host"] = details[1]
            site_dict["createdDate"] = details[7]
            hID = details[0]
            query_tulpa = methods.concatenate_sql().query_tulpa(hID)
            dat_tulpa = methods.Database_operation.connect(query_tulpa, conn_mem, 1)
            for tulpa in dat_tulpa:
                t_list = []
                t_single = dat_tulpa[1]
                t_list.append(str(t_single))
            site_dict["tulpas"] = str(t_list)
            list_of_site.append(site_dict)
        #construct_return dict to be returned and serializedd
        return_dict = {
            "pagesQuantity": len(list_of_site),
            "sites": list_of_site
        }
        print (site_dict)
        print (list_of_site)
        print (return_dict)
        #serialize return_dict to json
        data = json.dumps(site_dict, indent=4)
        return (data)
    #handle uploading request
    elif parsed_json['request'] == "uploading":
        #generate file names and path
        h_path = methods.gen_file_name(parsed_json, 2)
        f_name = methods.gen_file_name(parsed_json, 1)
        c_name = methods.gen_file_name(parsed_json, 3)
        host_path = os.path.join(path, h_path)
        #create host path
        os.mkdir(host_path)
        #concatenate sql for db operation
        sql_hmc_cover = methods.concatenate_sql.insert_HMC(parsed_json, f_name)
        sql_hmc_file = methods.concatenate_sql.insert_doc(parsed_json, c_name)
        sql_tulpa = methods.concatenate_sql.insert_tulpa(parsed_json)
        #decode base64 and write to folders
        with open(os.path.join(host_path, parsed_json["cover_name"]), "wb") as fh:
            fh.write(base64.decodebytes(parsed_json["cover"]))
        with open(os.path.join(host_path, parsed_json["cover_name"]), "wb") as fh:
            fh.write(base64.decodebytes(parsed_json["cover"]))
        #commit sql statements
        query_file_cover = methods.Database_operation(sql_hmc_cover,conn_mem, 2)
        query_hmc_file = methods.Database_operation(sql_hmc_file,conn_mem, 2)
        query_tulpa = methods.Database_operation(sql_tulpa,conn_mem, 2)
        return (query_file_cover+query_hmc_file+query_tulpa)
        
        
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