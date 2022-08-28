from crypt import methods
import methods_ohaul
import parser_ohaul
import asyncio
# json = """{
#             "request":"adminAuthentication",
#             "userName":"test",
#             "password":"test"
#            }"""
json = ("""
{"request":"mainList",
"page": 10
}""")
async def main():
  print (await parser_ohaul.parse_all(json))
asyncio.run(main())