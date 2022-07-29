import sqlite3
import os
import apsw
def init():
    if os.path.exists('database.db'):
        conn = apsw.Connection('database.db')
        memcon=apsw.Connection(":memory:")
        with memcon.backup("main", conn, "main") as backup:
            backup.step()
        return(memcon)
        
    else:
        #initialize/create connection to db
        conn = apsw.Connection('database.db')
        #initialize MainHMC table
        conn.execute('''CREATE TABLE MainHMC (hostID INTEGER PRIMARY KEY AUTOINCREMENT,
        h_name TEXT NOT NULL, h_age INTEGER, email TEXT, desc TEXT, path TEXT, v_status BOOLEAN NOT NULL DEFAULT FALSE,
        creation_time DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        #initialize RawData table           
        conn.execute('''CREATE TABLE RawData (dataID INTEGER PRIMARY KEY AUTOINCREMENT, 
        dataPath TEXT NOT NULL, upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        hID INTEGER, FOREIGN KEY(hID) REFERENCES MainHMC (hostID));''')
        #initialize Tulpas table
        conn.execute('''CREATE TABLE Tulpas (tulpaID INTEGER PRIMARY KEY AUTOINCREMENT,
        tulpaName TEXT NOT NULL, rec_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
        hID INTEGER, FOREIGN KEY(hID) REFERENCES MainHMC (HostID));''')
        #initialize assets table
        #type 1 = html
        #type 2 = cover
        conn.execute('''CREATE TABLE assets (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        assetPath TEXT NOT NULL, type TEXT NOT NULL, 
        hID INTEGER, FOREIGN KEY(hID) REFERENCES MainHMC (HostID));''')
        memcon=apsw.Connection(":memory:")
        with memcon.backup("main", conn, "main") as backup:
            backup.step() 
        
        conn.commit()
        conn.close()
        return (memcon)
    
