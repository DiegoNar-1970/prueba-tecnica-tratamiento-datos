import sqlite3
import pandas as pd
from config import Config
from logger import Logger
from impresor import Impresor


class DatabaseService:
    """
    Clase encargada de la conexión a la base de datos SQLite:
    creación de la tabla, inserción de los datos normalizados
    y consulta de lo ya insertado.
    """

    def __init__(self):
        self.logger = Logger()
        self.db_path = Config.DB_PATH

    def _conectar(self):
        """
        Método interno que abre y retorna una conexión a la base
        de datos SQLite. sqlite3.connect() crea el archivo .db
        automáticamente si todavía no existe.
        """
        return sqlite3.connect(self.db_path)

    def crear_tabla(self):
        """
        Crea la tabla 'productos' si no existe todavía.
        Usamos 'CREATE TABLE IF NOT EXISTS' precisamente para
        que no truene si el programa se ejecuta varias veces.
        """
        conexion = self._conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id TEXT PRIMARY KEY,
                rev TEXT,
                nombre TEXT,
                marca TEXT,
                presentacion TEXT,
                stock INTEGER
            )
        """)

        conexion.commit()
        conexion.close()

        self.logger.info("Tabla 'productos' verificada/creada correctamente")
        Impresor.exito("Tabla 'productos' lista en la base de datos")

    def insertar_datos(self, df):
        """
        Inserta en la tabla 'productos' el contenido de un
        DataFrame de pandas (el que genera normalizarInformacion()).

        Parámetros:
            df (pandas.DataFrame): datos ya normalizados, con las
                                    columnas id, rev, nombre, marca,
                                    presentacion, Stock.
        """
        conexion = self._conectar()

        # to_sql inserta el DataFrame completo en la tabla indicada.
        # if_exists="replace" borra la tabla y la vuelve a llenar cada
        # vez que corremos el programa, para que no se dupliquen filas
        # en cada ejecución durante las pruebas.
        df_renombrado = df.rename(columns={"Stock": "stock"})
        df_renombrado.to_sql("productos", conexion, if_exists="replace", index=False)

        conexion.close()

        self.logger.info(f"Se insertaron {len(df)} registros en la tabla 'productos'")
        Impresor.exito(f"Se insertaron {len(df)} registros en la base de datos")

    def consultar_datos(self):
        """
        Consulta todos los registros de la tabla 'productos' y los
        retorna como un DataFrame, además de imprimir un resumen
        en consola.
        """
        conexion = self._conectar()
        df = pd.read_sql_query("SELECT * FROM productos", conexion)
        conexion.close()

        self.logger.info(f"Consulta realizada: {len(df)} registros encontrados")
        Impresor.titulo(f"Registros en la base de datos: {len(df)}")
        print(df.head(10))  # muestra las primeras 10 filas como vista previa

        return df