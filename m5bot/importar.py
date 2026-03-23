import datetime

from pymysql.constants.FIELD_TYPE import SET

from libs.m5mysql import M5mysql
import csv
from libs.m5bot import M5bot


class Importar:
    def __init__(self):
        self.archivo = "csv/economicas_por_menor.csv"

    """def procesar(self):
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

                # mysql.query(sql, r)"""
    def procesar(self):
        # variable minuto y segundo
        minuto = datetime.datetime.now()
        bot = M5bot()
        msg = f"Iniciando importación de CSV {minuto}"
        bot.send_message(msg)

        mysql = M5mysql()
        sql = "DELETE FROM establecimiento"
        mysql.exec(sql)
        sql = "DELETE FROM colonia"
        mysql.exec(sql)
        sql = "DELETE FROM pagina_web"
        mysql.exec(sql)
        sql = "DELETE FROM tipo_empresa"
        mysql.exec(sql)
        sql = "DELETE FROM tipo_centro_comercio"
        mysql.exec(sql)
        sql = "DELETE FROM categoria_actividad"
        mysql.exec(sql)
        #---------------
        # leer el archivo self.archivo
        with open(self.archivo, newline='', encoding='utf-8') as File:
            rows = csv.reader(File)
            try:
                for r in rows:
                    print(r[0])
                    print(r[17])
                    sql = f"INSERT INTO `alcaldia`(`alcaldia`) VALUES ('{r[12]}');"
                    print(sql)
                    mysql.exec(sql)
                    # insertar en la base de datos
                    # mysql = M5mysql()

                    # mysql.query(sql, r)
            except:
                print("Error en la insercion de datos")
        with open(self.archivo, newline='', encoding='utf-8') as File:
            rows = csv.reader(File)
            try:

                # pagina_web
                for r in rows:
                    print(r[15])
                    sql = f"INSERT INTO `pagina_web`(`url`) VALUES ('{r[15]}');"
                    print(sql)
                    mysql.exec(sql)


                # para tipo_empresa
                for r in rows:
                    print(r[5])
                    sql = f"INSERT INTO `tipo_empresa`(`tipo_empresa`) VALUES ('{r[5]}');"
                    print(sql)
                    mysql.exec(sql)


                # para tipo_centro_comercio
                for r in rows:
                    print(r[7])

                    sql = f"INSERT INTO `tipo_centro_comercio`(`tipo_centro_comercio`) VALUES ('{r[7]}');"
                    print(sql)
                    mysql.exec(sql)

                # para categoria_actividad

                for r in rows:
                    print(r[3])

                    sql = f"INSERT INTO `categoria_actividad`(`categoria_actividad`) VALUES ('{r[3]}');"
                    print(sql)
                    mysql.exec(sql)

            #para colonia
                for r in rows:
                    print(r[14])
                    print(r[13])

                    sql = f"""
                    INSERT INTO `colonia`(`colonia`, `alcaldia_id`)
                    VALUES ('{r[14]}',
                        (SELECT alcaldia_id FROM alcaldia WHERE alcaldia = '{r[12]}')
                    );
                    """
                    print(sql)
                    mysql.exec(sql)

            except:
                print("Error en la insercion de datos")
        #---------------
        minuto = datetime.datetime.now()
        msg = f"Fin de la importación {minuto}"
        bot.send_message(msg)


importar_csv = Importar()
importar_csv.procesar()
