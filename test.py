from crypt import methods
import methods_ohaul
import parser_ohaul
import asyncio
# json = {
#             "request":"adminAuthentication",
#             "userName":"test",
#             "password":"test"
#            }
json = ("""
{"request":"adminList",
"token" : "ZWI1YzU1MDE4Y2E3MzVmMzE4ZmNkZmRmNjVmMDMyMjE2NWZlMDU0MTQ0MjYwZjIyMjM3ZGUyZTU5MjQ2ZmY0MQ==",
"page": 100
}""")
# print (type(methods_ohaul.admin_request.adminAuthentication(json)))

# print (methods_ohaul.admin_request.adminAuthentication(json))

parser_ohaul.parse_all(json)
