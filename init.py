from mysql import connector
import os

def init():
    database_obj = connector.connect(
  host="english-poetry.com",
  user="tulpa",
  password="c0912c8d3a270ada868bc56862354c8211086af917523e07b60bba30403c6417"
)
    #initialize/create connection to db
    cursor = database_obj.cursor()
    #initialize MainHMC table
    cursor.execute('''CREATE TABLE IF NOT EXISTS MainHMC (hostID INTEGER PRIMARY KEY AUTOINCREMENT,
    h_name TEXT NOT NULL, h_age INTEGER, email TEXT, desc TEXT, path TEXT, v_status BOOLEAN NOT NULL DEFAULT FALSE,
    creation_time DATETIME DEFAULT CURRENT_TIMESTAMP);''')
    #initialize RawData table           
    cursor.execute('''CREATE TABLE IF NOT EXISTS RawData (dataID INTEGER PRIMARY KEY AUTOINCREMENT, 
    dataPath TEXT NOT NULL, upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    hID INTEGER, FOREIGN KEY(hID) REFERENCES MainHMC (hostID));''')
    #initialize Tulpas table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tulpas (tulpaID INTEGER PRIMARY KEY AUTOINCREMENT,
    tulpaName TEXT NOT NULL, rec_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
    hID INTEGER, FOREIGN KEY(hID) REFERENCES MainHMC (HostID));''')
    #initialize assets table
    #type 1 = html
    #type 2 = cover
    cursor.execute('''CREATE TABLE IF NOT EXISTS assets (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
    assetPath TEXT NOT NULL, type TEXT NOT NULL, 
    hID INTEGER, FOREIGN KEY(hID) REFERENCES MainHMC (HostID));''')
    #commit
    cursor.commit()
    return (database_obj)
    
