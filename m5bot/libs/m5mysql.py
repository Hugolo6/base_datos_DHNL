from libs.m5config import M5config
import mysql.connector


class M5mysql:
    def __init__(self):
        config = M5config()
        conexion = config.get("mysql")
        self.host = conexion["host"]
        self.user = conexion["user"]
        self.password = conexion["password"]
        self.port = conexion["port"]
        self.database = conexion["database"]
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )
        self.cursor = self.conn.cursor(dictionary=True)
    def query(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self,sql):
        self.cursor.exec(sql)
        self.conn.commit()