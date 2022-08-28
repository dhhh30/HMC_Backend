from crypt import methods
import methods_ohaul
json = ("""
        {
            "request":"adminAuthentication",
            "userName":"test",
            "password":"test"
           }""")
print (methods_ohaul.admin_request.adminAuthentication(json))