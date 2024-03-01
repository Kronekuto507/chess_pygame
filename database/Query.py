import sqlite3

class Query:

    def __init__(self,db):
        self.__db = sqlite3.connect(db)
        self.__cursor = self.__db.cursor()
    
    def query(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
    
    def return_information(self):
        return self.__cursor.fetchall()
    
    def __del__(self):
        self.__db.close()

