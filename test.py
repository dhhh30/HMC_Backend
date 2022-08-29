from crypt import methods
import methods_ohaul
import parser_ohaul
import asyncio
json = {
            "request":"adminAuthentication",
            "userName":"test",
            "password":"test"
           }
# json = ("""
# {"request":"mainList",
# "page": 100
# }""")
print (type(methods_ohaul.admin_request.adminAuthentication(json)))

print (methods_ohaul.admin_request.adminAuthentication(json))
# async def main():
#     return await(parser_ohaul.parse_all(json))
# asyncio.run(main())