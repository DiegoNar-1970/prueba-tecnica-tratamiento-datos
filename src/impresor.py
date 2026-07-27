class Impresor:
    """
    Clase encargada de mostrar mensajes formateados en consola.

    Centraliza la forma en la que el programa se comunica con el
    usuario por consola, en vez de usar print() sueltos por todo
    el código.
    """

    @staticmethod
    def titulo(texto):
        """Imprime un encabezado destacado, útil para separar secciones."""
        print("\n" + "=" * 50)
        print(texto)
        print("=" * 50)

    @staticmethod
    def mensaje(texto):
        """Imprime un mensaje informativo normal."""
        print(f">> {texto}")

    @staticmethod
    def exito(texto):
        """Imprime un mensaje de éxito."""
        print(f"[OK] {texto}")

    @staticmethod
    def advertencia(texto):
        """Imprime una advertencia."""
        print(f"[ADVERTENCIA] {texto}")

    @staticmethod
    def error(texto):
        """Imprime un mensaje de error."""
        print(f"[ERROR] {texto}")