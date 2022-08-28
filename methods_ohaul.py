import time
from random import randrange
import base64
import os
import threading
import hashlib, secrets
import init
from datetime import datetime
import logging
import json
import init
import math


#paths
path = "/home/wwwroot/tulpa" 
public_htpath = "/home/wwwroot/tulpa"
special_auth_pass = "/home/wwwroot/tulpa/unverified"
#max concurrent thread
sema = threading.Semaphore(value=16)
#logging time function
def datetimenow():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return str("["+dt_string+"]")

#class for operating with DB
class database():
    #connect database for operation
    def connect(sql, conn, op_type):   
        #Cursor for above apsw connection object
        conn = init.init()
        cursor = conn.cursor()
        cursor.execute(sql)
        #op_type 1 = select
        #op_type 2 = insert
        if op_type == 1:
            data = cursor.fetchall()
            #returns fetched data in list
            cursor.close()
            return data
        elif op_type == 2:
            #returns last row id on insert
            cursor.close()
            conn.commit()
            return
        # elif op_type == 3:
        #     data = cursor.fetchone()
        #     cursor.close()
        #     return data
#SQL concaatenation
class sql_operation():
    #concatenate sql for inserting into HMC
    def insert_HMC(parsed_dict, host_path):
        sql = ("""INSERT INTO main_HMC (id, h_name, h_age, email, description, path, v_status, creation_time)
         VALUES (NULL, "{}","{}","{}","{}","{}","0",NULL)
         """.format(parsed_dict['host_name'], parsed_dict['host_age'], parsed_dict['email'], parsed_dict['introduce'], host_path , 0))
        return sql
    #concatenate sql for querying main HMC
    def query_main_List(pg_num):
        if pg_num == 1:
            row_num = pg_num-1
        else:
            pg_num -= 1
            row_num = pg_num*10
        sql = ("""SELECT path, creation_time, h_name, id FROM main_HMC LIMIT {}, 4""".format(row_num))
        return sql
    #concatenate sql for inserting into tulpa
    def insert_tulpa(i,  t_name, hID):
        sql = ("""INSERT INTO tulpas (id, tulpaName, hID) VALUES (NULL, "{}",{})""".format(t_name['tulpas_name'][i], hID))
        return (sql)
    #concatenate sql for querying tulpa
    def query_tulpa_main_List(hID):
        sql = ("""SELECT tulpaName FROM tulpas WHERE hID={}""".format(hID))
        return(sql) 
    def insert_doc(type , path, hID):
        sql = ("""INSERT INTO assets (id, assetPath, type, hID) VALUES (NULL,"{}","{}",{})""".format(path, type, hID))
        return sql
    #get total amount of row from table for pagination
    def get_total_row(table):
        sql = ("""SELECT COUNT(*) FROM {}""".format(table))
        return (sql)
    #concatenate sql query for inserting files into database
    def query_file(hID, type):
        sql = ("""SELECT assetPath FROM assets WHERE hID='{}' AND type='{}'""".format(hID,type))
        return sql
    def query_approve_hmc(hID):
        sql = ("""UPDATE * FROM main_HMC WHERE id='{}'""".format(hID[0]))
        return (sql)
    def get_host_id(h_name):
        sql =  """SELECT MAX(id) FROM main_HMC WHERE h_name = "{}" """.format(h_name)
        return sql
    
    def query_admin_list(pg_num, v_status):
        if pg_num == 1:
            row_num = pg_num-1
        else:
            pg_num -= 1
            row_num = pg_num*10
        
        if v_status != "":
            if v_status == True:
                v_status = 1
            if v_status == False:
                v_status = 0
            sql = ("""SELECT * FROM main_HMC WHERE v_status='{}' LIMIT {}, 4""".format(str(v_status), row_num))
            return sql
        else:
            sql = ("""SELECT * FROM mainHMC LIMIT {}, 4""".format(row_num))

            return sql
    def token_operation(token, op_code):
        #if the operation is to insert token into admin_token
        if op_code == 1:
            sql = ("""INSERT INTO admin_token (token, issued_time) VALUES('{}', NULL)""".format(token))
            return sql
        #if the operation is to query token from admin_token
        if op_code == 2:
            sql = ("""SELECT token FROM admin_token WHERE token = '{}'""".format(token))
            return sql
        if op_code == 3:
            sql = ("""SELECT EXISTS(SELECT * from admin_token WHERE token = '{}')""".format(token))
            return sql
class gen_file_name:
    def __init__(self, parsed_json, op_num):
        self.parsed_json = parsed_json
        self.op_num = op_num
    #generate file name
    def fname(self):
        ms = int(round(time.time() * 1000))
        rand_num = randrange(10)
        #generate file name
        if self.op_num == 1:
            final_file = (str(ms)+str(rand_num))
            return final_file
        #generate folder name
        if self.op_num == 2:
            final_file = (str(self.parsed_json["host_name"])+"-"+str(ms)+str(rand_num))
            return final_file
        #generate jpg
        if self.op_num ==3:
            final_file = (str("cover")+"-"+str(ms)+str(rand_num)+".jpg")
            return final_file
    
#file processing objects, RW
class file_operation(database):   
    def cover_database(c_name, query_hmc, conn_mem):
        sema.acquire()
        #sql for INSERTING into assets for HMC cover
        sql_hmc_cover = sql_operation.insert_doc("cover", c_name, query_hmc)
        #query for executing code for hmc cover
        database.connect(sql_hmc_cover,conn_mem, 2) 
        sema.release()
        return
    def uploading_tulpa( i, parsed_json, query_hmc, conn_mem):
        sema.acquire()
        sql_tulpa = sql_operation.insert_tulpa(i, parsed_json, query_hmc)
        print(sql_tulpa)
        database.connect(sql_tulpa, conn_mem, 2) 
        sema.release()
        return
    def uploading_webinput(f_name, query_hmc, conn_mem):
        sema.acquire()
        #concatenate sql for storing webinput records in asset table
        sql_hmc_webinput = sql_operation.insert_doc("webinput", f_name+".html", query_hmc)
        database.connect(sql_hmc_webinput, conn_mem, 2)
        sema.release()
        return
    def writing_image(host_path, parsed_json, i):
        sema.acquire()
        #decoding image from base64 and write them into perspective files
        image_file = open(os.path.join(host_path, str(parsed_json["imgs_names"])[i]), 'wb')
        image_file.write(base64.b64decode(str(parsed_json["imgs"][i])))
        image_file.close()
        sema.release()
        return
    #write cover to disk
    def writing_cover(host_path, parsed_json, cover_name):
        sema.acquire()
        cover_file = open(os.path.join(host_path, cover_name), 'wb')
        cover_file.write(base64.b64decode(parsed_json["cover"]))
        cover_file.close()
        sema.release()
        return

#general public requests objects
class general_request(database):
    def __init__(self):
        super().__init__()
    def mainList(parsed_json):
        conn_mem = init.init()
        #site dictionary
        site_dict = {}
        #concatenate sql for query hmc
        query_sql_hmc = sql_operation.query_main_List(int(parsed_json['page']))
        #concatenate sql for query main_hmc total row for pagination
        query_sql_hmc_trow = sql_operation.get_total_row("main_HMC")
        total_row =database.connect(query_sql_hmc_trow, conn_mem,1)
        #concatenate sql for query tulpa
        #query hmc
        dat_hmc = database.connect(query_sql_hmc, conn_mem,1)
        page_num = (total_row[0][0]/4)
        logging.debug(str(datetimenow())+"mainList total page number is: " + str(page_num))
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
            print (details[3])
            site_dict["h_name"] = details[2]
            site_dict["createdDate"] = str(details[1])
            sql_asset = sql_operation.query_file(str(details[3]), "webinput")
            print(sql_asset)
            query_asset = database.connect(sql_asset, conn_mem, 1)
            print(query_asset)
            site_dict["url"] = str(details[0]) +"/"+query_asset[0][0]
            query_tulpa = sql_operation.query_tulpa_main_List(details[3])
            dat_tulpa =database.connect(query_tulpa, conn_mem, 1)
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
        h_path = gen_file_name(parsed_json, 2).fname()
        f_name = gen_file_name(parsed_json, 1).fname()
        c_name = gen_file_name(parsed_json, 3).fname()
        host_path = (special_auth_pass+"/"+ h_path)
        #create host path
        os.mkdir(host_path)
        #concatenate sql for db operation
        sql_hmc = sql_operation.insert_HMC(parsed_json, host_path)
        print(sql_hmc)
        query_hmc = database.connect(sql_hmc, conn_mem, 2)
        #print(type(query_hmc))
        #spawn child process for querying cover
        h_name = str(parsed_json["host_name"])
        print (h_name)
        query_hmc_sql = sql_operation.get_host_id(h_name)
        print (query_hmc_sql)
        query_hmc = database.connect(query_hmc_sql, conn_mem, 1)[0]
        query_hmc_cover = threading.Thread(target=file_operation.cover_database, args=(c_name,query_hmc,conn_mem,))
        query_hmc_cover.start()
        #loop through tulpa list from json and perform Database INSERTs, spawning child process to speed up
        threads = []
        for i in range(len(parsed_json['tulpas_name'])):
            threads.append(threading.Thread(target=file_operation.uploading_tulpa, args=(i, parsed_json, query_hmc, conn_mem,)))
            threads[-1].start()
        print (threads)
        for thread in threads:
                thread.join()
        # for i in range(len(parsed_json['tulpas_name'])):
        #     file_operation.uploading_tulpa(i, parsed_json, query_hmc, conn_mem)
        #Writing webinput to asset
        sql_hmc_webinput = threading.Thread(target=file_operation.uploading_webinput, args=(f_name,query_hmc,conn_mem))
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
            threads.append(threading.Thread(target= file_operation.writing_image, args=(host_path,parsed_json,i)))
            threads[-1].start()
        for thread in threads:
            thread.join()
        # for i in range(len(parsed_json["imgs"])):
        #     file_operation.writing_image(host_path,parsed_json,i)
        #decode base64 and write to folders
        
        cover_thread = threading.Thread(target=file_operation.writing_cover, args=(host_path,parsed_json, c_name,))
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
#Admin operations
class admin(database):
    def __init__(self):
        database.__init__()
    def admin_authentication(pwd, uname):
        conn = init.init()
        #Detect if uname = email
        if "@" in uname == True:
            sql = """SELECT pwd_hash FROM admin_usr WHERE {} = '{}'""".format("email",uname)
        else:
            sql = """SELECT pwd_hash FROM admin_usr WHERE {} = '{}'""".format("uname",uname)
        #hash the input plain text pwd
        input_hash = hashlib.sha256(bytes(pwd, 'utf-8')).hexdigest()
        #query hashed pwd from database
        output_hash = database.connect(sql, conn, 1)
        #compare hashes
        return input_hash == output_hash[0][0]
    def admin_gen_token():
        #random sha256 generation function
        ms = int(round(time.time() * 1000))
        rand_num = randrange(100)
        token = hashlib.sha256(bytes(str(ms), "utf-8")).digest()
        token = hashlib.sha256(bytes(str(token)+str(rand_num) , "utf-8"))
        #encode sha256 into base64
        token = base64.b64encode(str(token).encode('utf-8')).decode("utf-8")

        return str(token)
            
    def admin_token_auth(token):
        token = str(database.connect(str(sql_operation.token_operation(token)), init.init(), 1).connect())
        
        pass

#admin requests objects
class admin_request(database):
    def adminList(parsed_json):
        conn_mem = init.init()
        #site dictionary
        site_dict = {}
        
        #concatenate sql for query hmc
        query_sql_hmc = sql_operation.query_main_List(int(parsed_json['page']))
        #concatenate sql for query main_hmc total row for pagination
        query_sql_hmc_trow =sql_operation.get_total_row("main_HMC")
        total_row = database.connect(query_sql_hmc_trow, conn_mem,1)
        #concatenate sql for query tulpa
        #query hmc
        dat_hmc =database.connect(query_sql_hmc, conn_mem,1)
        page_num = (total_row[0][0]/4)
        logging.debug(str(datetimenow())+"mainList total page number is: "+ str(page_num))
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
            sql_asset = sql_operation.query_file(str(details[3]), "webinput")
            print(sql_asset)
            query_asset = database.connect(sql_asset, conn_mem, 1)
            #print(query_asset)
            site_dict["url"] = str(details[0]) +"/"+query_asset[0][0]
            query_tulpa = sql_operation.query_tulpa_main_List(details[3])
            dat_tulpa =database.connect(query_tulpa, conn_mem, 1)
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
        compare_hash = admin.admin_authentication(parsed_json["password"], parsed_json["userName"])
        print(compare_hash, flush=True)
        if compare_hash == True:
            token =  admin.admin_gen_token()   
            token_sql = sql_operation.token_operation(token, 1)    
            database.connect(token_sql, conn_mem, 2)
            return_dict = {
                "request" : "adminAuthentication",
                "Success" :  compare_hash,
                "token": token
            }
            return_json = json.dumps(return_dict, indent=4)
            return str(return_json)
        else:
            return_dict= {
                "request" : "adminAuthentication",
                "Success" :  False
            }
            return_json = json.dumps(return_dict, indent=4) 
            return str(return_json)
    
    def adminApproval(parsed_json):
        pass
    def adminDenial(parsed_json):
        pass