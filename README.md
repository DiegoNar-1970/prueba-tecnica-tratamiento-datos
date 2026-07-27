# Prueba Técnica – Área de Automatizaciones y RPA (Emergia)

## Proyecto 1: Tratamiento de información, exportación y base de datos

Este proyecto lee un archivo JSON con información de productos, lo procesa
usando Programación Orientada a Objetos, exporta la información a archivos
Excel (uno crudo y uno normalizado) y finalmente inserta los datos
normalizados en una base de datos para su posterior consulta.

---

## 1. Requisitos previos

- **Python 3.9 o superior** (probado con Python 3.14.6)
- No se requiere ningún motor de base de datos externo: se usa **SQLite**,
  que viene incluido en la librería estándar de Python.

Para verificar tu versión de Python:

```bash
python --version
```

---

## 2. Estructura del proyecto

```
prueba-tecnica-emergia/
│
├── data/
│   ├── productos.json          # Archivo fuente de datos (entrada)
│   └── productos.db            # Base de datos SQLite (se genera al ejecutar)
│
├── logs/
│   └── proceso.log             # Registro de eventos del programa (se genera al ejecutar)
│
├── output/
│   ├── productos.xlsx              # Excel con los datos crudos extraídos del JSON
│   └── productos_normalizado.xlsx  # Excel con los datos ya normalizados
│
├── src/
│   ├── config.py                # Variables globales y constantes del sistema
│   ├── logger.py                # Registro de logs en archivo de texto
│   ├── impresor.py              # Mensajes formateados en consola
│   ├── normalized_services.py   # Lógica principal: lectura del JSON, exportación y normalización
│   ├── database_service.py      # Conexión, creación de tabla, inserción y consulta en SQLite
│   └── main.py                  # Punto de entrada del programa
│
├── venv/                        # Entorno virtual (no se sube a git)
├── requirements.txt             # Librerías necesarias del proyecto
└── README.md                    # Este archivo
```

---

## 3. Instalación y puesta en marcha (paso a paso)

Estos pasos funcionan igual en cualquier PC con Windows, macOS o Linux que
tenga Python instalado.

### 3.1 Clonar o descomprimir el proyecto

```bash
cd ruta/donde/quieras/el/proyecto
```

### 3.2 Crear el entorno virtual

El entorno virtual aísla las librerías de este proyecto del resto del sistema.

```bash
python -m venv venv
o py -3.14 -m venv venv  (por si no tienes las variables de entorno de python)
```

### 3.3 Activar el entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

Si se activó correctamente, verás `(venv)` al inicio de la línea de tu terminal.

### 3.4 Instalar las dependencias

```bash
pip install -r requirements.txt
```

Esto instala automáticamente `pandas` y `openpyxl`, las únicas librerías
externas que usa el proyecto (la conexión a base de datos usa `sqlite3`,
que ya viene incluido con Python).

### 3.5 Verificar que el archivo de datos esté en su lugar

Asegúrate de que el archivo `productos.json` esté ubicado en:

```
data/productos.json
```

### 3.6 Ejecutar el programa

```bash
cd src
python main.py
```

---

## 4. Qué hace el programa al ejecutarse

Al correr `main.py` se ejecuta, en orden, todo el flujo pedido en la prueba:

1. **Lectura y exportación (`jsonToExcel`)**
   Lee `data/productos.json`, extrae los campos `id, rev, nombre, uuid,
   marca, presentacion` y genera `output/productos.xlsx`. Imprime en
   consola el total de productos encontrados.

2. **Normalización (`normalizarInformacion`)**
   A partir de los mismos datos, genera un segundo archivo,
   `output/productos_normalizado.xlsx`, aplicando:
   - Se agrega el campo **Stock** con un valor aleatorio entre 1 y 10.
   - Se elimina el campo **uuid**.
   - Todo registro cuyo campo **marca** sea `"SIN MARCA"` se reemplaza por
     `"Pruebas Emergia"`.

3. **Base de datos (`DatabaseService`)**
   - Crea (si no existe) la tabla `productos` en `data/productos.db`.
   - Inserta en ella los datos ya normalizados.
   - Consulta la tabla completa y muestra en consola una vista previa de
     los primeros 10 registros.

Puedes revisar visualmente el archivo `data/productos.db` instalando la
extensión de VS Code **"SQLite Viewer"**.

---

## 5. Explicación de cada módulo (clases)

| Archivo | Responsabilidad |
|---|---|
| `config.py` | Centraliza rutas de archivos y valores constantes del proyecto (ubicación del JSON, carpetas de salida, campos requeridos, rango de stock, textos de reemplazo de marca). Evita "hardcodear" valores repetidos en el resto del código. |
| `logger.py` | Registra mensajes de tipo INFO, WARNING y ERROR en `logs/proceso.log`, con fecha y hora, para trazabilidad del proceso. |
| `impresor.py` | Centraliza los mensajes que se muestran en consola, dándoles un formato consistente (títulos, éxito, advertencias, errores). |
| `normalized_services.py` | Clase principal del tratamiento de datos: lee el JSON, exporta el Excel crudo (`jsonToExcel`) y genera el Excel normalizado (`normalizarInformacion`). |
| `database_service.py` | Encapsula toda la interacción con la base de datos: creación de tabla, inserción y consulta. |
| `main.py` | Orquesta la ejecución del programa llamando a las clases anteriores en el orden correcto. |

---

## 6. Decisiones de diseño

- **Motor de base de datos:** el enunciado solicita "base de datos SQL" sin
  especificar el motor. Se optó por **SQLite** por ser una base de datos
  embebida (un solo archivo, sin necesidad de instalar ni configurar un
  servidor externo), lo que facilita que cualquier evaluador pueda ejecutar
  el proyecto en su propia máquina sin pasos adicionales de infraestructura.
- **`if_exists="replace"` al insertar:** cada vez que se ejecuta el programa,
  la tabla se reconstruye con los datos más recientes, evitando duplicados
  al correr el proceso varias veces durante las pruebas.
- **Uso de `.get()` en la lectura del JSON:** se accede a los campos del
  diccionario con `.get(campo, valor_por_defecto)` en vez de indexación
  directa, para que el programa no falle si algún registro llegara a tener
  un campo faltante.

---

## 7. Autor

Diego — Prueba técnica para el área de Automatizaciones y RPA, Emergia (2026).

