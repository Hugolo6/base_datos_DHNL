from libs.m5config import M5config
from libs.m5bot import M5bot
from libs.m5mysql import M5mysql
import csv

class Importar:
    def __init__(self):
        self.archivo = "csv/economicas_por_menor.csv"
    def procesar (self):
        #variable con mitutos y segundos
        minuto = datetime.datetime.now()
        print(minuto)
        bot = M5bot()
        msg = "iniciando importacion"
        bot.send_message(msg)

        mysql = M5mysql()
        sql = "select * from establecimiento"
        mysql.exec(sql)

        # ---------------
        # leer el archivo self.archivo
        with open(self.archivo, newline='', encoding='utf-8') as File: #endoding es para que al migrar me muestre los caracteres especiales
            row = csv.reader(File)
            for r in row:
                print(r[0])
                print(r[6])
                sql = f("INSERT INTO 'establecimiento' ('establecimienito') VALUES ('(r[0])')")

                mysql.exec(sql)

                # insertar en la base de datos
                # mysql = M5mysql()
                # sql = "insert into directorio_menor values (null, %s, %s, %s, %s, %s, %s, %s)"
                # mysql.query(sql, row)
        # ---------------

        msg = "fin de la importacion"
        bot.send_message(msg)
        minuto = datetime.datetime.now()


        # importacion de todas los
        # parte mimi

importar_csv = Importar()
importar_csv.procesar()
