from crypt import methods
import methods_ohaul
import parser_ohaul
json = """{
            "request":"adminAuthentication",
            "userName":"test",
            "password":"test"
           }"""
print (parser_ohaul(json))