import json
import pandas as pd
from config import Config
from logger import Logger
from impresor import Impresor
import random

class normalized_services:
    """
    Clase encargada de leer la información de productos desde el
    archivo JSON, tratarla y exportarla a un archivo Excel.

    Aquí se concentra la lógica de "tratamiento de información y
    exportación"""

    def __init__(self):
        """
        Constructor: inicializa el logger que va a usar esta clase
        y prepara un atributo para guardar los datos ya leídos,
        de forma que otros métodos (como la normalización) los
        puedan reutilizar sin tener que leer el JSON otra vez.
        """
        self.logger = Logger()
        self.datos = None  # aquí quedará guardada la lista de productos ya leída

    def leer_json(self):
        """
        Lee el archivo JSON definido en Config.JSON_PATH y lo
        carga en memoria como una lista de diccionarios de Python.

        Retorna:
            list: lista de productos tal como vienen en el JSON.
        """
        self.logger.info(f"Leyendo archivo JSON: {Config.JSON_PATH}")

        with open(Config.JSON_PATH, "r", encoding="utf-8") as f:
            self.datos = json.load(f)

        self.logger.info(f"Se leyeron {len(self.datos)} registros del JSON")
        return self.datos

    def jsonToExcel(self):
        """
        Método principal de esta clase: toma los datos del JSON,
        extrae únicamente los campos requeridos (id, rev, nombre,
        uuid, marca, presentacion) y los exporta a un archivo Excel.

        También imprime en consola el total de productos encontrados,
        tal como lo pide el enunciado.
        """
        if self.datos is None:
            self.leer_json()

        filas = []

        for producto in self.datos:
            valor = producto.get("value", {}) #probemos cono funciona esto 

            fila = {
                "id": valor.get("_id", ""),
                "rev": valor.get("_rev", ""),
                "nombre": valor.get("nombre", ""),
                "uuid": valor.get("uuid", ""),
                "marca": valor.get("marca", ""),
                "presentacion": valor.get("presentacion", "")
            }
            filas.append(fila)

        # Convertimos la lista de diccionarios en un DataFrame de pandas,
        # que es básicamente una tabla en memoria.
        df = pd.DataFrame(filas, columns=Config.CAMPOS_EXCEL)

        # Nos aseguramos de que exista la carpeta de salida antes de escribir
        Config.crear_carpetas()

        # Exportamos el DataFrame a un archivo Excel, sin la columna de
        # índice numérico que pandas agrega por defecto (index=False)
        df.to_excel(Config.EXCEL_PRODUCTOS, index=False)

        total = len(df)
        Impresor.exito(f"Archivo Excel generado en: {Config.EXCEL_PRODUCTOS}")
        Impresor.titulo(f"Total de productos encontrados: {total}")

        self.logger.info(f"Excel generado con {total} productos en {Config.EXCEL_PRODUCTOS}")

        return df

    def normalizarInformacion(self):
        """
        Toma los datos ya cargados del JSON y genera un segundo
        Excel normalizado:
            - Agrega el campo 'Stock' con un valor aleatorio (1-10)
            - Elimina el campo 'uuid'
            - Reemplaza el valor 'SIN MARCA' por 'Pruebas Emergia'
              en el campo 'marca'
        """
        if self.datos is None:
            self.leer_json()

        filas = []

        for producto in self.datos:
            valor = producto.get("value", {})

            marca = valor.get("marca", "")
            if marca == Config.MARCA_SIN_MARCA:
                marca = Config.MARCA_REEMPLAZO

            fila = {
                "id": valor.get("_id", ""),
                "rev": valor.get("_rev", ""),
                "nombre": valor.get("nombre", ""),
                "marca": marca,
                "presentacion": valor.get("presentacion", ""),
                "Stock": random.randint(Config.STOCK_MIN, Config.STOCK_MAX)
            }
            filas.append(fila)

        # Nótese: 'uuid' ya no aparece en las columnas -> queda excluido
        columnas = ["id", "rev", "nombre", "marca", "presentacion", "Stock"]
        df = pd.DataFrame(filas, columns=columnas)

        Config.crear_carpetas()
        df.to_excel(Config.EXCEL_NORMALIZADO, index=False)

        Impresor.exito(f"Archivo normalizado generado en: {Config.EXCEL_NORMALIZADO}")
        self.logger.info(f"Excel normalizado generado con {len(df)} registros")

        return df