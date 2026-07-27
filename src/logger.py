import os
import datetime
from config import Config


class Logger:
    """
    Clase encargada de registrar mensajes de log en un archivo de texto.

    Cada vez que se llama a un método (info, error, etc.), se agrega
    una línea al archivo de log con fecha, hora, nivel del mensaje
    y el contenido del mensaje.
    """

    def __init__(self, nombre_archivo="proceso.log"):
        """
        Constructor de la clase.

        Parámetros:
            nombre_archivo (str): nombre del archivo donde se guardarán
                                   los logs. Por defecto 'proceso.log'.
        """
        Config.crear_carpetas()
        self.ruta_log = os.path.join(Config.LOGS_DIR, nombre_archivo)

    def _escribir(self, nivel, mensaje):
        """
        Método interno (privado por convención, de ahí el guion bajo)
        que arma la línea de log y la escribe en el archivo.

        No se llama directamente desde fuera de la clase; los métodos
        públicos (info, error, warning) lo usan por debajo.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] [{nivel}] {mensaje}\n"

        with open(self.ruta_log, "a", encoding="utf-8") as f:
            f.write(linea)

    def info(self, mensaje):
        """Registra un mensaje informativo (flujo normal del programa)."""
        self._escribir("INFO", mensaje)

    def warning(self, mensaje):
        """Registra una advertencia (algo raro, pero no un error crítico)."""
        self._escribir("WARNING", mensaje)

    def error(self, mensaje):
        """Registra un error."""
        self._escribir("ERROR", mensaje)