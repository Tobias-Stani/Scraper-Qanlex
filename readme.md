# Scraper de Casos Judiciales del Poder Judicial

## 📝 Descripción del Proyecto

Herramienta automatizada para extracción de datos de expedientes judiciales del sitio web del Poder Judicial Nacional, con almacenamiento en base de datos MySQL.

## 🗂️ Descripción Detallada de Scripts

### 1. `scraper.py`

#### Funcionalidad Principal
- Automatiza la extracción de información de casos judiciales

#### Acciones Específicas
- Navega al sitio web del Poder Judicial Nacional
- Realiza búsqueda con filtro de palabra clave "residuos"
- Resuelve CAPTCHA de forma manual
- Extrae información de cada expediente, incluyendo:
  - Número de expediente
  - Jurisdicción
  - Dependencia
  - Situación actual
  - Carátula (descripción del caso)
  - Movimientos del expediente
  - Actores y demandados

#### Salida
- Genera archivo `expedientes.json` con todos los datos extraídos

### 2. `uploader.py`

#### Funcionalidad Principal
- Carga automatizada de datos extraídos a base de datos MySQL

#### Acciones Específicas
- Lee archivo `expedientes.json`
- Establece conexión con base de datos MySQL
- Inserta datos en tres tablas relacionales:
  1. `expedientes`: Información general del caso
  2. `movimientos`: Historial de movimientos del expediente
  3. `participantes`: Listado de actores y demandados

#### Procesamiento de Datos
- Limpia y formatea fechas
- Maneja transacciones SQL para integridad de datos
- Elimina archivo JSON después de carga exitosa

### Requisitos Previos
- Git
- Docker
- Docker Compose

### 1. Clonar Repositorio

```bash
git clone https://github.com/[tu-usuario]/scraper-casos-judiciales.git
cd scraper-casos-judiciales
```

### 2. Levantar Infraestructura Docker

```bash
# Construir contenedores
docker-compose build

# Iniciar servicios
docker-compose up -d
```

### 3. Acceso a phpMyAdmin

- **URL**: http://localhost:9080
- **Servidor**: `db`
- **Usuario**: `scraperuser`
- **Contraseña**: `scraperpass`

### 4. Crear Estructura de Base de Datos

#### Script de Creación de Tablas

```sql
CREATE TABLE expedientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expediente VARCHAR(255),
    jurisdiccion VARCHAR(255),
    dependencia VARCHAR(255),
    situacion_actual VARCHAR(255),
    caratula VARCHAR(255)
);

CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expediente_id INT,
    fecha DATE,
    tipo VARCHAR(255),
    detalle TEXT,
    FOREIGN KEY (expediente_id) REFERENCES expedientes(id)
);

CREATE TABLE participantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expediente_id INT,
    tipo VARCHAR(255),
    nombre VARCHAR(255),
    FOREIGN KEY (expediente_id) REFERENCES expedientes(id)
);
```

### 5. Pasos en phpMyAdmin

1. Iniciar sesión en http://localhost:9080
2. Seleccionar base de datos `scraper_data`
3. Ir a pestaña "SQL"
4. Pegar script de creación de tablas
5. Ejecutar consulta

### 6. Ejecutar Scraper

```bash
# Dentro del contenedor
python scraper.py

# Luego
python guardarDb.py
```

## 🔍 Detalles del Proyecto

### Componentes
- `scraper.py`: Extracción de datos judiciales
- `uploader.py`: Carga a base de datos MySQL
- Docker para infraestructura

### Tecnologías
- Python
- Selenium
- MySQL
- Docker

## 🚨 Consideraciones

- Resolución **manual** de CAPTCHA
- Conexión a internet estable
- Instalación de Google Chrome
