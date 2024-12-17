# Scraper de Casos Judiciales

## Descripción del Proyecto

Este proyecto automatiza la extracción de casos judiciales del sitio web del Poder Judicial Nacional, realizando las siguientes tareas:
- Scraping web de expedientes judiciales
- Extracción de datos detallados
- Almacenamiento en formato JSON
- Carga de datos a base de datos MySQL

## Flujo de Trabajo

### 1. Scraping de Datos
- Script: `scraper.py`
- Función: Extraer información de casos judiciales
- Salida: Archivo `src/expedientes.json`

### 2. Carga de Datos 
- Script: `uploader.py`
- Función: Subir datos extraídos a base de datos MySQL
- Acción: Elimina archivo JSON después de la carga

## Requisitos Previos

- Python 3.8+
- Google Chrome
- Docker y Docker Compose
- Dependencias:
  - selenium
  - webdriver-manager
  - mysql-connector-python

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

## Uso Manual (Sin Docker)

### 1. Ejecutar Scraper

```bash
python scraper.py
```

🚨 **IMPORTANTE**: 
- Durante la ejecución, será necesario resolver manualmente el CAPTCHA
- Los datos se guardarán en `src/expedientes.json`

### 2. Subir Datos a MySQL

```bash
python uploader.py
```

🔍 **Proceso Detallado**:
1. El scraper extrae los casos
2. Se genera un archivo `expedientes.json`
3. El uploader carga los datos en MySQL
4. El archivo JSON se elimina automáticamente

## Despliegue con Docker

### Requisitos

- Docker
- Docker Compose

### Comandos Docker

```bash
# Construir e iniciar contenedores
docker-compose up --build

# Ejecutar scraper dentro del contenedor
docker-compose exec scraper python /app/src/scraper.py

# Ejecutar uploader dentro del contenedor
docker-compose exec scraper python /app/uploader.py
```

## Configuración de Base de Datos

### Estructura de Tablas MySQL

1. `expedientes`
```sql
CREATE TABLE expedientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expediente VARCHAR(255),
    jurisdiccion VARCHAR(255),
    dependencia VARCHAR(255),
    situacion_actual TEXT,
    caratula TEXT
);
```

2. `movimientos`
```sql
CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expediente_id INT,
    fecha DATE,
    tipo VARCHAR(255),
    detalle TEXT,
    FOREIGN KEY (expediente_id) REFERENCES expedientes(id)
);
```

3. `participantes`
```sql
CREATE TABLE participantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expediente_id INT,
    tipo ENUM('ACTOR', 'DEMANDADO'),
    nombre VARCHAR(255),
    FOREIGN KEY (expediente_id) REFERENCES expedientes(id)
);
```

## Configuración de Conexión

Credenciales predeterminadas:
- **Host**: 172.29.0.2
- **Usuario**: scraperuser
- **Contraseña**: scraperpass
- **Base de Datos**: scraper_data

## Componentes del Proyecto

- `scraper.py`: Extracción web de casos
- `uploader.py`: Carga de datos a MySQL
- `Dockerfile`: Configuración del entorno
- `docker-compose.yml`: Orquestación de servicios

## Consideraciones

- Resolver CAPTCHA manualmente
- Verificar conexión a internet
- Comprobar instalación de Chrome
- Validar credenciales de base de datos

## Contribución

1. Fork del repositorio
2. Crear rama de características
3. Commit de cambios
4. Push de rama
5. Abrir Pull Request

