import mysql.connector
from mysql.connector import Error

class StoreData(commands.cog):
    def __init__(self, client):
        super().__init__()
    
    try:
        connection = mysql.connector.connect(host = 'localhost', database = 'image_bot', user = 'root', password = 'root')
        
        mysql_Create_Table_Query = """CREATE TABLE DB_""" + str(guild) + """(
                                    Id int(11) NOT NULL AUTO_INCREMENT,
                                    User varchar(250) NOT NULL, 
                                    Text var cahr(5000) NOT NULL,
                                    Image_Link varchar(5000) NOT NULL,
                                    PRIMARY KEY (ID))"""

        cursor = connection.cursor()
        result = cursor.execute(mysql_Create_Table_Query)
    
    except mysql.connector.Error as error:
        print("Failed to Create Table")
