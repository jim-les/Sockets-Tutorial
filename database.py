import sqlite3



class Database:
    def __init__(self):
        self.conn =  sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.createTable()

    def createTable(self):
        query = """
        CREATE TABLE IF NOT EXISTS recv_messages (
            Id INTEGER PRIMARY KEY,
            message TEXT
        )
        """
        self.c.execute(query)
        self.conn.commit()

    def insertMessage(self, message):
        query = "INSERT INTO recv_messages (message) VALUES (?)"
        self.c.execute(query, (message,))
        self.conn.commit()
        print("Message insert into db")
    
    def getAllMessages(self):
        query = "SELECT message FROM recv_messages"
        self.c.execute(query)
        messages = self.c.fetchall()
        return [message[0] for message in messages]



