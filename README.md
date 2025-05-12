# Freshservice Asset Management Tool

## Descripción

Freshservice Asset Management Tool es una aplicación diseñada para facilitar la gestión y obtención de información detallada de activos desde Freshservice. Esta herramienta proporciona tanto una interfaz web como una interfaz de línea de comandos para realizar consultas y gestionar activos en Freshservice.

## Características Principales

- **Consulta de Activos por ID**: Obtén información detallada de activos mediante sus identificadores
- **Búsqueda Avanzada**: Localiza activos por usuario, departamento o ubicación
- **Información de Componentes**: Accede a datos específicos de componentes (CPU, RAM, HDD, NIC)
- **Exportación de Datos**: Exporta los resultados a Excel para análisis posterior
- **Importación desde Excel**: Carga IDs de activos desde archivos Excel
- **Interfaz Web Intuitiva**: Accede a todas las funcionalidades a través de un navegador web
- **Caché de Consultas**: Optimización de rendimiento mediante almacenamiento local de resultados frecuentes

## Estructura del Proyecto

```
freshservice-tools/
├── fstools.py                # Punto de entrada para CLI
├── run.py                    # Punto de entrada para la interfaz web
├── requirements.txt          # Dependencias del proyecto
├── .env                      # Archivo de configuración con credenciales (crear manualmente)
├── freshservice/             # Módulo principal del backend
│   ├── __init__.py
│   ├── api.py
│   ├── freshservice_manager.py
│   └── ...
└── web/                      # Módulo de interfaz web
    ├── __init__.py
    ├── app.py
    ├── forms.py
    ├── routes.py
    ├── static/
    └── templates/
```

## Requisitos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Credenciales de API de Freshservice

## Instalación

1. **Clonar el repositorio**:

```bash
git clone https://github.com/tu-usuario/freshservice-tools.git
cd freshservice-tools
```

2. **Crear y activar entorno virtual**:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

4. **Configurar credenciales**:

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
FRESHSERVICE_SUBDOMAIN=tu-subdominio
FRESHSERVICE_API_KEY=tu-api-key
SECRET_KEY=una-clave-secreta-para-flask
```

## Uso del Portal Web

### Iniciar la Aplicación Web

Para iniciar el portal web, ejecuta el siguiente comando:

```bash
python run.py
```

Esto iniciará el servidor Flask en modo de desarrollo en `http://localhost:5000`.

### Acceso a la Aplicación

1. Abre tu navegador web
2. Visita `http://localhost:5000`
3. El PIN de debug es: `123-456-789` (útil para depuración)

### Funcionalidades del Portal Web

#### Búsqueda por ID de Activo

- Accede a `/search_id`
- Introduce los IDs de activos separados por comas o en rangos (ej: "143-150,155")
- Selecciona los componentes y la información adicional que deseas obtener
- Visualiza los resultados en pantalla o descárgalos en Excel

#### Búsqueda por Criterios

- Accede a `/search_criteria`
- Busca activos por nombre de usuario, departamento o ubicación
- Filtra los resultados según tus necesidades
- Exporta a Excel los resultados obtenidos

#### Carga de Archivos

- Accede a `/upload`
- Sube archivos Excel con IDs de activos en la primera columna
- Procesa estos IDs para obtener información detallada
- Descarga los resultados en formato Excel

## Componentes Principales de la Aplicación Web

### Rutas (routes.py)

- **/** - Página principal
- **/search_id** - Búsqueda de activos por ID
- **/search_criteria** - Búsqueda de activos por usuario, departamento o ubicación
- **/upload** - Carga de archivos Excel con IDs
- **/download_excel** - Descarga de resultados en formato Excel
- **/download_criteria_excel** - Descarga de resultados de búsqueda por criterios

### Formularios (forms.py)

- **AssetForm** - Formulario para búsqueda por ID
- **SearchForm** - Formulario para búsqueda por criterios
- **FileUploadForm** - Formulario para carga de archivos

### Plantillas (templates/)

- **base.html** - Plantilla base con estructura común
- **index.html** - Página de inicio
- **search_id.html** - Interfaz de búsqueda por ID
- **search_criteria.html** - Interfaz de búsqueda por criterios
- **upload.html** - Interfaz de carga de archivos

## Personalización y Configuración

### Variables de Entorno

Las siguientes variables de entorno pueden ser configuradas en el archivo `.env`:

- **FRESHSERVICE_SUBDOMAIN**: Subdominio de tu instancia de Freshservice
- **FRESHSERVICE_API_KEY**: Clave API para autenticación
- **SECRET_KEY**: Clave secreta para seguridad de Flask
- **CACHE_TIMEOUT**: Tiempo de expiración de la caché en segundos (opcional)
- **DEBUG**: Modo de depuración (True/False) (opcional)

### Configuración del Servidor

Por defecto, la aplicación se ejecuta en modo de desarrollo. Para entornos de producción, se recomienda:

1. Deshabilitar el modo debug en `run.py`
2. Utilizar un servidor WSGI como Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "web:app"
```

## Solución de Problemas

### Errores de Conexión API

Si experimentas errores de conexión con la API de Freshservice:

1. Verifica que las credenciales en `.env` sean correctas
2. Comprueba tu conexión a internet
3. Verifica si hay límites de tasa (rate limits) en tu cuenta de Freshservice

### Problemas de Rendimiento

Si la aplicación funciona lentamente:

1. Verifica la cantidad de IDs consultados (procesamiento de grandes volúmenes puede ser lento)
2. Comprueba el sistema de caché para asegurar que funciona correctamente
3. Utiliza la opción de combinar consultas de CPU y RAM para reducir llamadas API

## Licencia

Este proyecto está licenciado bajo [incluir licencia aquí]

