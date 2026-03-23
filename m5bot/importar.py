from libs.m5mysql import M5mysql
import csv

class Importar:
    def __init__(self):
        self.archivo = "csv/directorio_menor.csv"

    def procesar(self):
        # variable minuto y segundo
        minuto = datetime.datetime.now()
        bot = M5bot()
        msg = f"Iniciando importación de CSV {minuto}"
        bot.send_message(msg)

        mysql = M5mysql()
        sql = "truncate table establecimiento"
        mysql.exec(sql)
        #---------------
        # leer el archivo self.archivo
        with open(self.archivo, newline='', encoding='utf-8') as File:
            rows = csv.reader(File)
            for r in rows:
                print(r[0])
                print(r[6])
                sql = f"INSERT INTO `establecimiento`(`establecimiento`) VALUES ('{r[0]}');"
                print(sql)
                mysql.exec(sql)
                # insertar en la base de datos
                # mysql = M5mysql()

                # mysql.query(sql, r)
        #---------------
        minuto = datetime.datetime.now()
        msg = f"Fin de la importación {minuto}"
        bot.send_message(msg)

importar_csv = Importar()
importar_csv.procesar()
