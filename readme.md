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

## 🔧 **Requisitos Previos**
Antes de ejecutar el proyecto, asegúrate de tener instalados:

- **Git**
- **Docker** y **Docker Compose**
- **Selenium**: Para la automatización del navegador.
- **Webdriver-Manager**: Gestión automática de **ChromeDriver**.
- **MySQL Connector for Python**: Para interactuar con la base de datos.

---

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

## 🚨 **Consideraciones**
- Resolución **manual** de CAPTCHA.  
- Conexión a **internet estable**.  
- Instalación de **Google Chrome** en la máquina host.  


