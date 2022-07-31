import methods
import sqlite3
for i in range (100):
    string = ("test"+str(i))
    tuple_String = [string,string,string,string,string,string]
    sql = ("""INSERT INTO MainHMC VALUES (NULL,?, ?, ?,?,?,?,NULL);""")
    sql1 = ("""INSERT INTO Tulpas VALUES (NULL,?, NULL, ?);""")
    conn = sqlite3.connect('database.db')
    print(sql)
    conn.execute(sql, tuple_String)
    conn.execute(sql1, [string,i])
    conn.commit()