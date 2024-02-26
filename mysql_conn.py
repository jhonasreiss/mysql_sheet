import mysql.connector

class MySQlConnect():

    def __init__(self, database,host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def connect_sql(self):
        self.config = mysql.connector.connect(host=self.host,
                                                  database=self.database,
                                                  port=self.port,
                                                  username=self.username,
                                                  password=self.password)
        self.conn = self.config.cursor()
        print('Está conectado!')


    def consult_data(self):
        query = "SELECT * FROM registro;"
        self.conn.execute(query)
        result = self.conn.fetchall()
        return result

    def close_connection(self):
        self.conn.close()
        self.config.close()