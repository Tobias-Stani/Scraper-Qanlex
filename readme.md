# Scraper de Casos Judiciales del Poder Judicial

## 📝 Descripción del Proyecto

Este proyecto es una herramienta de extracción automatizada de información de casos judiciales del sitio web del Poder Judicial Nacional. Su objetivo principal es:

- Recopilar datos de expedientes judiciales
- Extraer información detallada como número de expediente, jurisdicción, partes intervinientes, movimientos, etc.
- Almacenar la información de manera estructurada en una base de datos MySQL

## 🗂️ Archivos del Proyecto

### 1. `scraper.py`
- **Función**: Extracción de datos judiciales
- **Acciones**:
  - Navega por el sitio web del Poder Judicial
  - Resuelve manualmente el CAPTCHA
  - Busca casos relacionados con "residuos"
  - Extrae información de cada expediente
  - Guarda los datos en un archivo `expedientes.json`

### 2. `guardarDb.py`
- **Función**: Carga de datos a base de datos MySQL
- **Acciones**:
  - Lee el archivo `expedientes.json`
  - Inserta datos en tres tablas:
    1. `expedientes`: Información general del caso
    2. `movimientos`: Registros y movimientos del expediente
    3. `participantes`: Actores y demandados
  - Elimina el archivo JSON después de la carga

## 🐳 Configuración con Docker

### Requisitos Previos
- Docker
- Docker Compose

### Pasos para Levantar el Proyecto

1. **Construir Contenedores**
```bash
docker-compose build
```

2. **Iniciar Servicios**
```bash
docker-compose up
```

### Lo que Sucede Automáticamente

- Crea un contenedor MySQL
- Genera la base de datos `scraper_data`
- Crea las tablas necesarias
- Levanta un contenedor con la aplicación de scraping
- Habilita phpMyAdmin para administración (puerto 9080)

### Ejecución de Scripts

Los scripts se ejecutarán de forma automatizada:

1. **Scraper**
```bash
python scraper.py
```

2. **Uploader**
```bash
python guardarDb.py
```

## 🔍 Detalles Técnicos

### Base de Datos

Tablas creadas:
- `expedientes`: Datos generales del caso
- `movimientos`: Historial de movimientos
- `participantes`: Actores y demandados

### Tecnologías

- Lenguaje: Python
- Web Scraping: Selenium
- Base de Datos: MySQL
- Contenedores: Docker

## 🚨 Consideraciones Importantes

- Resolución **manual** de CAPTCHA
- Conexión a internet estable
- Instalación de Google Chrome

## 📦 Instalación de Dependencias

```bash
pip install -r requirements.txt
```
