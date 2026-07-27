import os

class Config:
    """
    Clase encargada de centralizar las variables globales y constantes
    del proyecto: rutas de archivos, nombres de carpetas, etc.

    Al tener todo esto en un solo lugar, evitamos escribir rutas
    "a mano" repetidas en varias clases (esto es lo que se conoce
    como evitar valores "hardcodeados").
    """

    # Carpeta raíz del proyecto (un nivel arriba de src/)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Rutas de entrada y salida
    JSON_PATH = os.path.join(BASE_DIR, "data", "productos.json")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    DB_PATH = os.path.join(BASE_DIR, "data", "productos.db")

    # Nombres de los archivos que vamos a generar
    EXCEL_PRODUCTOS = os.path.join(OUTPUT_DIR, "productos.xlsx")
    EXCEL_NORMALIZADO = os.path.join(OUTPUT_DIR, "productos_normalizado.xlsx")

    # Campos que se deben extraer del JSON al primer Excel
    CAMPOS_EXCEL = ["id", "rev", "nombre", "uuid", "marca", "presentacion"]

    # Rango para el campo Stock aleatorio (parte de normalización)
    STOCK_MIN = 1
    STOCK_MAX = 10

    # Valor que reemplaza a "SIN MARCA"
    MARCA_SIN_MARCA = "SIN MARCA"
    MARCA_REEMPLAZO = "Pruebas Emergia"

    @staticmethod
    def crear_carpetas():
        """
        Verifica que existan las carpetas de salida y logs.
        Si no existen, las crea. Esto evita errores si alguien
        clona el proyecto y esas carpetas no vienen incluidas
        (por ejemplo, porque Git no versiona carpetas vacías).
        """
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(Config.LOGS_DIR, exist_ok=True)