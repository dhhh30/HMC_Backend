from crypt import methods
import methods_ohaul
import parser_ohaul
import asyncio
# json = {
#             "request":"adminAuthentication",
#             "userName":"test",
#             "password":"test"
#            }
# json = {"request":"adminList",
# "token" : "ZWI1YzU1MDE4Y2E3MzVmMzE4ZmNkZmRmNjVmMDMyMjE2NWZlMDU0MTQ0MjYwZjIyMjM3ZGUyZTU5MjQ2ZmY0MQ==",
# "vStatus" : "",
# "page": 100
# }
# print (type(methods_ohaul.admin_request.adminAuthentication(json)))

# print (methods_ohaul.admin_request.adminAuthentication(json))
json = ("""{
    "request":"uploading",
    "host_name":"Dylan",
    "tulpas_name" : ["veronica", "example"],
    "host_age": "15",
    "email": "chendylan680@gmail.com",
    "file_name": "dchen4",
    "cover_name": "cover",
    "imgs": ["imagebrurbub","image placeholder"],
    "imgs_names": ["random.jpg","placeholder.jpg"],
    "introduce": "Hello guys",
    "webInput": "<h1>This is dang intresting</h1>",
    "cover": "PGgxPuWXqOWXqOWXqDwvaDE+",
    "file": "PGgxPuWXqOWXqOWXqDwvaDE+"

}""")
print(parser_ohaul.parse_all(json))
