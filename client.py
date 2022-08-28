#Test WS client
import asyncio
import websockets
# ws = websocket.WebSocket()
# ws.connect("ws://localhost:2186")
# ws.send("""{
# "request":"mainList", "page": 1
# }""")
# print(ws.recv())
# ws.close()
import time
import logging
from time import sleep
start = time.time()
import hashlib, secrets
from random import randrange
import base64
logging.basicConfig(level=logging.INFO)
# input_int = input("input page number:")
# json = ("""{
#     "request":"uploading",
#     "host_name":"Dylan",
#     "tulpas_name" : ["veronica", "example"],
#     "host_age": "15",
#     "email": "chendylan680@gmail.com",
#     "file_name": "dchen4",
#     "cover_name": "cover",
#     "imgs": ["imagebrurbub","image placeholder"],
#     "imgs_names": ["random.jpg","placeholder.jpg"],
#     "introduce": "Hello guys",
#     "webInput": "<h1>This is dang intresting</h1>",
#     "cover": "PGgxPuWXqOWXqOWXqDwvaDE+",
#     "file": "PGgxPuWXqOWXqOWXqDwvaDE+"

# }""")
# json = ("""
#         {
#             "request":"adminAuthentication",
#             "userName":"test",
#             "password":"test"
#            }""")
# json = ("""
# {"request":"mainList",
# "page": 10
# }""")
def admin_authentication(pwd, uname):
    # conn = init()
    #Detect if uname = email
    if "@" in uname == True:
        sql = """SELECT pwd_hash FROM admin_usr WHERE {} = '{}'""".format("email",uname)
    else:
        sql = """SELECT pwd_hash FROM admin_usr WHERE {} = '{}'""".format("uname",uname)
    #hash the input plain text pwd
    input_hash = hashlib.sha256(pwd.encode('utf-8'))
    #query hashed pwd from database
    #print (h.hexdigest())
    output_hash = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
    #compare hashes
    print(str(input_hash.hexdigest()))
    return str(input_hash.hexdigest()) == output_hash
print (admin_authentication("test", "test"))
# print (admin_gen_token())
# async def test():
#     async with websockets.connect("ws://english-poetry.com:2186") as websocket:
#         await websocket.send(json)
#         retur_msg = await websocket.recv()

#     return retur_msg
# for i in range(1000):
#     print(i)
#     print(asyncio.run(test()))
#     # except asyncio.exceptions.TimeoutError:
#     #     print(asyncio.run(test()))
#     # sleep(0.1)
# end = time.time()
# print("1000 queries completed in:"+ str(end - start))
