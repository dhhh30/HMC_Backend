from mariadb import connect
import os

def init():
    database_obj = connect(
  host="english-poetry.com",
  user="tulpa",
  password="c0912c8d3a270ada868bc56862354c8211086af917523e07b60bba30403c6417",
  database="tulpas"
)
#     #initialize/create connection to db
#     cursor = database_obj.cursor()
#     #initialize MainHMC table
#     cursor.execute('''CREATE TABLE 'main_HMC' (
# 	'id' INT NOT NULL AUTO_INCREMENT,
# 	'h_name' TEXT,
# 	'h_age' INT,
# 	'email' TEXT,
# 	'desc' TEXT,
# 	'path' TEXT,
# 	'v_status' BOOLEAN DEFAULT '0',
# 	'creation_time' TIMESTAMP DEFAULT 'CURRENT_TIMESTAMP'
# );''')
#     #initialize RawData table           
#     cursor.execute('''CREATE TABLE IF NOT EXISTS RawData (dataID INTEGER AUTO_INCREMENT PRIMARY KEY, 
#     dataPath TEXT NOT NULL, upload_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     hID INTEGER, FOREIGN KEY(hID) REFERENCES MainHMC (hostID));''')
#     #initialize Tulpas table
#     cursor.execute('''CREATE TABLE IF NOT EXISTS Tulpas (tulpaID INTEGER PRIMARY KEY AUTO_INCREMENT,
#     tulpaName TEXT NOT NULL, rec_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
#     hID INTEGER, FOREIGN KEY(hID) REFERENCES MainHMC (HostID));''')
#     #initialize assets table
#     #type 1 = html
#     #type 2 = cover
#     cursor.execute('''CREATE TABLE IF NOT EXISTS assets (ID INTEGER PRIMARY KEY AUTO_INCREMENT, 
#     assetPath TEXT NOT NULL, type TEXT NOT NULL, 
#     hID INTEGER, FOREIGN KEY(hID) REFERENCES MainHMC (HostID));''')
#     #commit
#     cursor.commit()
    return (database_obj)
    
