# 🏡️ **Proyecto de Web Scraping Judicial**

## 📝 **Descripción del Proyecto**
Herramienta automatizada para la extracción de datos de **expedientes judiciales** del sitio web del **Poder Judicial Nacional**, con almacenamiento en una base de datos **MySQL**.

---

## 🗂️ **Descripción Detallada de Scripts**

### 1. `scraper.py`
#### 🛠️ **Funcionalidad Principal**
- Automatiza la extracción de información de casos judiciales.

#### 🚀 **Acciones Específicas**
- Navega al sitio web del **Poder Judicial Nacional**.
- Realiza búsquedas con el filtro de palabra clave **"residuos"**.
- Resuelve el **CAPTCHA** de forma **manual**.
- Extrae información detallada de cada expediente, incluyendo:
  - **Número de expediente**  
  - **Jurisdicción**  
  - **Dependencia**  
  - **Situación actual**  
  - **Carátula** (descripción del caso)  
  - **Movimientos del expediente**  
  - **Actores y demandados**

#### 📂 **Salida**
- Genera un archivo `expedientes.json` con todos los datos extraídos.

---

### 2. `guardarDb.py`
#### 🛠️ **Funcionalidad Principal**
- Automatiza la carga de datos extraídos en una base de datos **MySQL**.

#### 🚀 **Acciones Específicas**
- Lee el archivo `expedientes.json`.
- Establece conexión con la base de datos **MySQL**.
- Inserta los datos en tres tablas relacionales:
  1. **`expedientes`**: Información general del caso.  
  2. **`movimientos`**: Historial de movimientos del expediente.  
  3. **`participantes`**: Listado de actores y demandados. 
- Elimina el archivo.
- Cierra la conexion.  

#### 🔧 **Procesamiento de Datos**
- Limpia y formatea las fechas.
- Maneja **transacciones SQL** para asegurar la integridad de los datos.
- Elimina el archivo JSON después de una carga exitosa.

---

### 📝 **Correspondencia de los Datos Extraídos con la Consigna**

A continuación, se detalla cómo cada campo extraído por el scraper corresponde con los requisitos establecidos en la consigna del proyecto:

| **Campo Extraído**      | **Descripción**                                                      | **Requisito de la Consigna**                              |
|-------------------------|----------------------------------------------------------------------|----------------------------------------------------------|
| **Expediente**           | Número único que identifica el expediente judicial.                  | El scraper extrae el número del expediente judicial.      |
| **Dependencia**          | Dependencia judicial encargada de gestionar el expediente.           | Corresponde a la **Dependencia** del caso.                |
| **Demandante**           | Actores o personas que inician el caso judicial.                     | Extraído como parte de los **actores** en el expediente.  |
| **Demandado**            | Personas o entidades contra las cuales se inicia el proceso judicial. | Extraído como parte de los **demandados** en el expediente.|
| **Carátula**             | Breve descripción o resumen del caso judicial.                       | Corresponde a la **carátula** o descripción del caso.     |
| **Tipo de Demanda**      | Tipo de caso o acción legal (por ejemplo, "Acción Civil").            | Corresponde al **tipo de demanda** o acción judicial.     |
| **Juzgado o Tribunal**   | Juzgado o tribunal que está encargado del expediente.                 | Extraído de la información de **jurisdicción** y **dependencia**. |
| **Fechas Relevantes**    | Fechas importantes asociadas al expediente (por ejemplo, fechas de audiencias, resoluciones). | Las **fechas** de los **movimientos** de cada expediente se extraen para registrar los eventos claves. |

---

## 🔧 **Requisitos Previos**
Antes de ejecutar el proyecto, asegúrate de tener instalados:

- **Git**
- **Docker** y **Docker Compose**
- **Selenium**: Para la automatización del navegador.
- **Webdriver-Manager**: Gestión automática de **ChromeDriver**.
- **MySQL Connector for Python**: Para interactuar con la base de datos.

---

### 🔍 **Ejemplo de cómo se extraen los datos**

- **Expediente**: El scraper extrae el número de expediente judicial directamente de la página web del Poder Judicial Nacional.
- **Dependencia**: Se extrae de la jurisdicción correspondiente que lleva el caso.
- **Demandante y Demandado**: Los actores (demandantes) y demandados se extraen de las listas asociadas al expediente judicial.
- **Carátula**: Es la breve descripción del caso que se obtiene directamente de la información disponible en la página.
- **Tipo de Demanda**: Este dato es derivado de la descripción de la causa (carátula) y otras fuentes disponibles en el expediente.
- **Juzgado o Tribunal**: La jurisdicción y dependencia del caso indican el juzgado o tribunal que maneja el expediente.
- **Fechas Relevantes**: El scraper extrae las fechas de los movimientos del expediente, como resoluciones, audiencias, entre otros.

---

### 📂 **Relación con la Base de Datos**

- **Expediente**: Almacenado en la tabla `expedientes` en el campo `expediente`.
- **Dependencia**: Almacenado en la tabla `expedientes` en el campo `dependencia`.
- **Demandante y Demandado**: Almacenados en la tabla `participantes` con la información del `tipo` (actor o demandado) y `nombre`.
- **Carátula**: Almacenado en la tabla `expedientes` en el campo `caratula`.
- **Tipo de Demanda**: Este campo puede ser extraído de la carátula o los movimientos, y se puede almacenar en el campo `situacion_actual` de la tabla `expedientes`.
- **Juzgado o Tribunal**: Extraído de la jurisdicción, se almacena en la tabla `expedientes` en el campo `jurisdiccion`.
- **Fechas Relevantes**: Almacenadas en la tabla `movimientos`, con la fecha y el tipo de movimiento correspondiente.



## 🚀 **Pasos de Instalación y Ejecución**

1. **Clonar el repositorio**:  
   ```bash
   git clone https://github.com/Tobias-Stani/Scraper-Qanlex.git
   ```

2. **Moverse al directorio del proyecto**:  
   ```bash
   cd Scraper-Qanlex
   ```

3. **Construir la imagen de Docker**:  
   ```bash
   docker-compose build
   ```

4. **Levantar el contenedor**:  
   ```bash
   docker-compose up
   ```

5. **Instalar dependencias (local)**:  
   ```bash
   pip install selenium webdriver-manager mysql-connector-python
   ```

6. **Configurar conexión MySQL**:  
   - Verificar las credenciales y la IP del servidor en el archivo `docker-compose.yml`.
   - Configurar los datos de acceso en los scripts.

7. **Crear base de datos y estructura**:  
   Ejecutar la siguiente estructura SQL en MySQL:

   ```sql
    -- La tabla `expedientes` almacena información básica del expediente judicial.
    CREATE TABLE expedientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        expediente VARCHAR(255),           -- El número del expediente judicial
        jurisdiccion VARCHAR(255),         -- La jurisdicción del caso
        dependencia VARCHAR(255),          -- Dependencia que lleva el caso
        situacion_actual VARCHAR(255),     -- Estado o situación actual del expediente
        caratula VARCHAR(255)              -- Descripción breve del caso
    );
    
    -- La tabla `movimientos` almacena los movimientos del expediente judicial.
    CREATE TABLE movimientos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        expediente_id INT,                 -- Relacionado con el ID de la tabla `expedientes`
        fecha DATE,                        -- Fecha del movimiento
        tipo VARCHAR(255),                 -- Tipo de movimiento (ej. "Resolución", "Audiencia", etc.)
        detalle TEXT,                      -- Descripción del movimiento
        FOREIGN KEY (expediente_id) REFERENCES expedientes(id) -- Relación con `expedientes`
    );
    
    -- La tabla `participantes` almacena los actores y demandados en el expediente.
    CREATE TABLE participantes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        expediente_id INT,                 -- Relacionado con el ID de la tabla `expedientes`
        tipo VARCHAR(255),                 -- Tipo de participante (actor, demandado, etc.)
        nombre VARCHAR(255),               -- Nombre del participante
        FOREIGN KEY (expediente_id) REFERENCES expedientes(id) -- Relación con `expedientes`
    );
   ```

8. **Ejecutar los scripts**:  
   ```bash
   python scraper.py
   python guardarDb.py
   ```

---

## 💡 **Posibles Mejoras**
1. **Optimización del script principal** para reducir los tiempos de ejecución.  
2. Implementación de **resolución automática del CAPTCHA**.  
3. Mejor arquitectura para **AWS** con despliegue automatizado.  
4. Uso de **variables de entorno** para eliminar credenciales **hardcodeadas**.

---

## 🔍 **Detalles del Proyecto**

### 📦 **Componentes**
- **`scraper.py`**: Extracción de datos judiciales.  
- **`guardarDb.py`**: Carga de datos en MySQL.  
- **Docker**: Infraestructura para facilitar el despliegue.

### 🛠️ **Tecnologías Utilizadas**
- **Python**
- **Selenium**
- **MySQL**
- **Docker**

---

## 🚨 **Consideraciones Importantes**

- **Resolución Manual de CAPTCHA**: 
  - Durante la ejecución del script `scraper.py`, se requiere intervención manual para resolver el CAPTCHA. Asegúrate de estar disponible para completar esta tarea cuando se te solicite.

- **Una vez resuelto el CAPTCHA**:
  - Una vez resuelto el CAPTCHA, el usuario no necesitará hacer nada más. El proceso está completamente automatizado y el programa te indicará cualquier acción adicional que deba tomarse.
  
- **Conexión a Internet Estable**:
  - La herramienta depende de una conexión a internet para acceder al sitio web y obtener los datos. Asegúrate de tener una conexión estable antes de ejecutar los scripts.

- **Instalación de Google Chrome**:
  - Se debe tener **Google Chrome** instalado en la máquina host, ya que **Selenium** utiliza este navegador para la automatización.

- **Ejecutar el Script `scraper.py` Varias Veces**:
  - Es posible que necesites ejecutar el script `scraper.py` varias veces para asegurarte de que se obtengan todos los expedientes disponibles. Esto es especialmente útil si el número de casos es grande y la búsqueda puede no devolver todos los resultados en una sola ejecución.

- **Credenciales de Base de Datos**:
  - Asegúrate de configurar correctamente las credenciales de acceso a la base de datos. Por defecto, las credenciales son las siguientes:
  
    ```bash
    DB_HOST=172.30.0.2
    DB_USER=scraperuser
    DB_PASSWORD=scraperpass
    DB_NAME=scraper_data
    ```

  - Verifica que estos valores coincidan con los configurados en tu entorno o en tu archivo `docker-compose.yml`.



