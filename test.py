import methods
import sqlite3
from mariadb import connect
database_obj = connect(
  host="english-poetry.com",
  user="tulpa",
  password="c0912c8d3a270ada868bc56862354c8211086af917523e07b60bba30403c6417",
  database="tulpas"
)

for i in range (100):
    string = ("test"+str(i))
    tuple_String = [string,string,string,string,string,string]
    sql = ("""INSERT INTO main_HMC (id, h_name, h_age, email, description, v_status, creation_time) VALUES (NULL, '{}', '{}', '{}','{}', '0', NULL)""".format(string, '12' ,string,string))
    sql1 = ("""INSERT INTO tulpas VALUES (NULL,'{}', '{}', NULL);""".format(string, i+1))
    conn = database_obj.cursor()
    print(sql)
    conn.execute(sql)
    database_obj.commit()
    conn.execute(sql1)
    #conn.execute(sql1, [string,i])
    database_obj.commit()