from mariadb import connect
import os
#10.8.0.1:3306
def init():
    database_obj = connect(
  host="english-poetry.com",
  user="tulpa",
  password="c0912c8d3a270ada868bc56862354c8211086af917523e07b60bba30403c6417",
  database="tulpas"
)

    return (database_obj)
    
