# Documentación de Freshservice Asset Management Tool

## Propósito de la Aplicación

Freshservice Asset Management Tool es una aplicación diseñada para facilitar la gestión y obtención de información detallada de activos desde Freshservice. Permite a los administradores de TI y otros usuarios autorizados:

- Obtener información detallada de activos y sus componentes
- Buscar activos por usuario, departamento o ubicación
- Listar departamentos y ubicaciones en la organización
- Importar IDs de activos desde archivos Excel
- Exportar resultados en formatos Excel o txt para análisis posterior
- Acceder a todas estas funciones tanto por línea de comandos como por una interfaz web intuitiva

La herramienta se integra directamente con la API de Freshservice para obtener datos en tiempo real, almacenando en caché resultados frecuentes para mejorar el rendimiento y reducir las llamadas a la API.

## Estructura de Carpetas

```
freshservice-tools/
├── .env                      # Archivo de configuración con credenciales
├── .gitignore                # Archivo de configuración de Git
├── README.md                 # Documentación principal
├── fstools.py                # Punto de entrada para CLI
├── requirements.txt          # Dependencias del proyecto
├── run.py                    # Punto de entrada para la interfaz web
├── .venv/                    # Entorno virtual (generado)
├── logs/                     # Directorio para archivos de registro
├── .cache/                   # Caché para resultados de API
├── freshservice/             # Módulo principal del backend
│   ├── __init__.py           # Inicialización del módulo
│   ├── api.py                # Cliente para la API de Freshservice
│   ├── asset_manager.py      # Gestión de activos
│   ├── cache_manager.py      # Sistema de caché
│   ├── component_manager.py  # Gestión de componentes
│   ├── config.py             # Configuración general
│   ├── data_exporter.py      # Exportación de datos
│   ├── data_processor.py     # Procesamiento de datos
│   ├── department_manager.py # Gestión de departamentos
│   ├── excel_manager.py      # Importación/exportación Excel
│   ├── export_manager.py     # Gestión de exportaciones
│   ├── freshservice_manager.py # Clase principal de gestión
│   ├── location_manager.py   # Gestión de ubicaciones
│   ├── performance_monitor.py # Monitoreo de rendimiento
│   ├── search_manager.py     # Búsqueda de activos
│   ├── user_manager.py       # Gestión de usuarios
│   └── managers/             # Gestores específicos
│       ├── __init__.py        
│       ├── department_manager.py
│       ├── location_manager.py  
│       ├── user_manager.py
│       └── assets/            # Gestión específica de activos
└── web/                      # Módulo de interfaz web
    ├── __init__.py           # Inicialización de Flask
    ├── app.py                # Aplicación principal
    ├── forms.py              # Formularios para la interfaz
    ├── routes.py             # Rutas y controladores
    ├── static/               # Archivos estáticos (CSS, JS, imágenes)
    │   ├── css/
    │   └── img/
    └── templates/            # Plantillas HTML
        ├── base.html         # Plantilla base
        ├── index.html        # Página principal
        ├── search.html       # Página de búsqueda
        ├── search_criteria.html # Búsqueda por criterios
        ├── search_id.html    # Búsqueda por ID
        └── upload.html       # Subida de archivos
```

## Tecnologías Utilizadas

### Backend
- **Python 3.x**: Lenguaje de programación principal
- **Flask**: Framework web ligero para la interfaz de usuario
- **Requests**: Biblioteca para realizar peticiones HTTP a la API de Freshservice
- **Pandas**: Manipulación y análisis de datos
- **openpyxl**: Manejo de archivos Excel
- **python-dotenv**: Gestión de variables de entorno
- **colorama**: Formato de texto en consola
- **tqdm**: Barras de progreso para operaciones largas

### Frontend
- **Flask-Bootstrap**: Integración de Bootstrap con Flask
- **WTForms**: Manejo de formularios
- **Flask-WTF**: Integración de WTForms con Flask
- **HTML/CSS/JavaScript**: Tecnologías web estándar
- **Bootstrap**: Framework CSS para diseño responsive

### Almacenamiento
- **Sistema de archivos**: Almacenamiento en caché local
- **Excel**: Importación y exportación de datos

### Integración
- **Freshservice API**: API REST para obtener información de activos y otros datos

## Arquitectura del Sistema

### Backend

La arquitectura del backend sigue un diseño modular con separación clara de responsabilidades:

1. **Capa de API (api.py)**
   - Maneja la comunicación con Freshservice API
   - Implementa autenticación y manejo de errores
   - Gestiona límites de tasa (rate limiting)
   - Proporciona cache para optimizar peticiones

2. **Capa de Gestión (freshservice_manager.py)**
   - Coordina las operaciones entre los distintos módulos
   - Implementa la lógica de negocio principal
   - Expone las funcionalidades tanto a la CLI como a la interfaz web

3. **Gestores Especializados**
   - **asset_manager.py**: Gestión de activos
   - **component_manager.py**: Gestión de componentes de activos
   - **location_manager.py**: Gestión de ubicaciones
   - **user_manager.py**: Gestión de usuarios
   - **department_manager.py**: Gestión de departamentos
   - **search_manager.py**: Búsqueda de activos por diferentes criterios

4. **Utilidades**
   - **cache_manager.py**: Sistema de caché para optimizar peticiones
   - **excel_manager.py**: Manejo de archivos Excel
   - **data_processor.py**: Procesamiento de datos
   - **performance_monitor.py**: Monitoreo de rendimiento
   - **data_exporter.py**: Exportación de datos

### Frontend

La interfaz web utiliza una arquitectura MVC (Modelo-Vista-Controlador) basada en Flask:

1. **Modelo**: Los datos provienen del módulo `freshservice` que actúa como la capa de modelo
2. **Vista**: Plantillas HTML con Flask-Bootstrap en el directorio `templates/`
3. **Controlador**: Rutas definidas en `routes.py` que manejan las peticiones HTTP

El flujo de datos es:
1. El usuario interactúa con los formularios web
2. Las rutas en `routes.py` procesan estas peticiones
3. Se invoca la funcionalidad apropiada del backend a través de `FreshServiceManager`
4. Los resultados se pasan a las plantillas que los renderizan para el usuario

## Pasos para Levantar el Entorno

### 1. Requisitos Previos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Credenciales de API de Freshservice

### 2. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/freshservice-tools.git
cd freshservice-tools
```

### 3. Crear y Activar Entorno Virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Credenciales

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
FRESHSERVICE_SUBDOMAIN=tu-subdominio
FRESHSERVICE_API_KEY=tu-api-key
SECRET_KEY=una-clave-secreta-para-flask
```

Donde:
- `tu-subdominio` es el subdominio de tu instancia de Freshservice (ej. si tu URL es https://empresa.freshservice.com, el subdominio es "empresa")
- `tu-api-key` es la clave API generada desde Freshservice
- `una-clave-secreta-para-flask` es una cadena aleatoria para seguridad de la aplicación web

### 6. Crear Directorios Necesarios

Los directorios para caché y logs se crearán automáticamente al iniciar la aplicación, pero puedes crearlos manualmente:

```bash
mkdir -p .cache logs
```

### 7. Iniciar la Aplicación

#### Para la interfaz de línea de comandos:

```bash
python fstools.py -h  # Ver opciones disponibles
```

#### Para la interfaz web:

```bash
python run.py
```

La aplicación web estará disponible en http://localhost:5000

### 8. Configuración de Base de Datos (No requerida)

Esta aplicación no utiliza una base de datos tradicional. En su lugar:
- Almacena datos en caché en el sistema de archivos (directorio `.cache`)
- Utiliza Freshservice como "base de datos" externa a través de su API
- Los resultados se exportan a archivos Excel o txt

## Flujo de Procesamiento de Datos

### 1. Interfaz de Línea de Comandos (fstools.py)

1. **Análisis de Argumentos**: 
   - `parse_arguments()` procesa los argumentos de línea de comandos
   - Valida y normaliza los parámetros proporcionados

2. **Inicialización**:
   - Crea una instancia de `FreshServiceManager`
   - Configura el entorno de ejecución (logs, caché)

3. **Procesamiento**:
   - Según los argumentos, ejecuta la operación solicitada:
     - Búsqueda de activos por ID
     - Búsqueda por criterios (usuario, departamento, ubicación)
     - Listado de departamentos o ubicaciones
     - Importación de IDs desde Excel

4. **Obtención de Datos**:
   - Realiza llamadas a la API de Freshservice
   - Utiliza caché para optimizar rendimiento
   - Procesa datos para formato requerido

5. **Salida**:
   - Exporta resultados según formato solicitado (Excel, txt)
   - Muestra información en consola si se solicitó

### 2. Interfaz Web (run.py → web/app.py → web/routes.py)

1. **Inicialización**:
   - Flask carga la configuración y rutas
   - Se establece la conexión con el backend a través de `FreshServiceManager`

2. **Procesamiento de Peticiones**:
   - El usuario completa y envía formularios
   - Las rutas en `routes.py` manejan las peticiones POST/GET
   - Se validan los datos de entrada

3. **Ejecución de Operaciones**:
   - Se invoca la funcionalidad correspondiente en el backend
   - Se procesan los datos utilizando los mismos módulos que la CLI

4. **Presentación de Resultados**:
   - Los datos se pasan a las plantillas Jinja2
   - Se renderizan para mostrar al usuario
   - Se ofrecen opciones para exportar/descargar resultados

### 3. Flujo de Datos con la API de Freshservice

1. **Autenticación**:
   - Se utilizan las credenciales del archivo `.env`
   - Se envían con cada petición a la API

2. **Peticiones a la API**:
   - El módulo `api.py` maneja las peticiones HTTP
   - Implementa manejo de errores y reintentos
   - Gestiona límites de tasa (rate limiting)

3. **Caché de Resultados**:
   - Las respuestas se almacenan en caché local
   - Se reutilizan para reducir llamadas a la API
   - Se invalidan según configuración (tiempo de vida)

4. **Procesamiento de Respuestas**:
   - Los datos JSON se convierten a estructuras Python
   - Se filtran y procesan según los requerimientos
   - Se combinan datos de múltiples endpoints cuando es necesario

5. **Exportación**:
   - Los datos procesados se convierten al formato solicitado
   - Se guardan en archivos o se envían al navegador

Este flujo asegura eficiencia en el procesamiento de datos y una experiencia de usuario fluida tanto en la línea de comandos como en la interfaz web.
