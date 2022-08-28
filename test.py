from crypt import methods
import methods_ohaul
import parser_ohaul
import asyncio
json = """{
            "request":"adminAuthentication",
            "userName":"test",
            "password":"test"
           }"""
# json = ("""
# {"request":"mainList",
# "page": 100
# }""")
print (type(methods_ohaul.admin.admin_authentication("test", "test")))
print (methods_ohaul.admin.admin_authentication("test", "test"))
# async def main():
#   print (await parser_ohaul.parse_all(json))
# asyncio.run(main())