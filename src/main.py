from normalized_services import normalized_services
from database_service import DatabaseService
from impresor import Impresor


def main():
    Impresor.titulo("PRUEBA TÉCNICA - TRATAMIENTO DE PRODUCTOS")

    servicio = normalized_services()
    servicio.jsonToExcel()
    df_normalizado = servicio.normalizarInformacion()

    db = DatabaseService()
    db.crear_tabla()
    db.insertar_datos(df_normalizado)
    db.consultar_datos()


if __name__ == "__main__":
    main()