import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import os  # Para eliminar el archivo

class SubidorDeBaseDeDatos:
    def __init__(self, host, usuario, contrasena, base_de_datos):
        """
        Inicializa los parámetros de conexión a la base de datos.
        
        :param host: Host del servidor MySQL
        :param usuario: Nombre de usuario de MySQL
        :param contrasena: Contraseña de MySQL
        :param base_de_datos: Nombre de la base de datos
        """
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.base_de_datos = base_de_datos
        self.conexion = None

    def _conectar(self):
        """Establece una conexión con la base de datos MySQL."""
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.contrasena,
                database=self.base_de_datos
            )
            if self.conexion.is_connected():
                print("Conexión exitosa a la base de datos")
        except Error as e:
            print(f"Error al conectar a la base de datos MySQL: {e}")
            raise

    def _cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Conexión a la base de datos cerrada")

    def limpiar_fecha(self, fecha):
        """Limpia el texto de fecha antes de intentar convertirla a formato de fecha."""
        if fecha:
            # Eliminar cualquier texto innecesario antes de la fecha
            fecha = fecha.replace('Fecha:', '').strip()  # Remueve 'Fecha:' y cualquier espacio adicional
        return fecha

    def subir_expedientes(self, archivo_datos_scrapeados):
        """
        Subir los datos de expedientes scrapeados a la base de datos.
        
        :param archivo_datos_scrapeados: Archivo JSON que contiene los datos scrapeados
        """
        try:
            # Asegurar la conexión a la base de datos
            self._conectar()
            cursor = self.conexion.cursor()

            # Leer los datos scrapeados
            with open(archivo_datos_scrapeados, 'r', encoding='utf-8') as archivo:
                datos_scrapeados = json.load(archivo)

            # Preparar y ejecutar la consulta SQL para cada expediente
            for caso in datos_scrapeados:
                # Insertar en la tabla expedientes
                consulta_expediente = """
                INSERT INTO expedientes 
                (expediente, jurisdiccion, dependencia, situacion_actual, caratula) 
                VALUES (%s, %s, %s, %s, %s)
                """
                valores_expediente = (
                    caso.get('expediente', ''),
                    caso.get('jurisdiccion', ''),
                    caso.get('dependencia', ''),
                    caso.get('situacion_actual', ''),
                    caso.get('caratula', '')
                )
                
                cursor.execute(consulta_expediente, valores_expediente)
                expediente_id = cursor.lastrowid

                # Insertar movimientos
                if caso.get('registros_tabla'):
                    consulta_movimientos = """
                    INSERT INTO movimientos 
                    (expediente_id, fecha, tipo, detalle) 
                    VALUES (%s, %s, %s, %s)
                    """
                    valores_movimientos = [
                        (expediente_id, 
                         datetime.strptime(self.limpiar_fecha(registro['fecha']), '%d/%m/%Y').date() if registro['fecha'] else None, 
                         registro['tipo'], 
                         registro['detalle']) 
                        for registro in caso.get('registros_tabla', [])
                    ]
                    cursor.executemany(consulta_movimientos, valores_movimientos)

                # Insertar participantes (actores y demandados)
                consulta_participantes = """
                INSERT INTO participantes 
                (expediente_id, tipo, nombre) 
                VALUES (%s, %s, %s)
                """
                valores_participantes = []
                
                # Añadir actores
                valores_participantes.extend([
                    (expediente_id, 'ACTOR', actor) 
                    for actor in caso.get('actores', [])
                ])
                
                # Añadir demandados
                valores_participantes.extend([
                    (expediente_id, 'DEMANDADO', demandado) 
                    for demandado in caso.get('demandados', [])
                ])
                
                if valores_participantes:
                    cursor.executemany(consulta_participantes, valores_participantes)

            # Confirmar la transacción
            self.conexion.commit()
            print("¡Datos subidos exitosamente!")

            # Eliminar el archivo después de subir los datos
            if os.path.exists(archivo_datos_scrapeados):
                os.remove(archivo_datos_scrapeados)  # Elimina el archivo
                print(f"El archivo {archivo_datos_scrapeados} ha sido eliminado exitosamente!")

        except Error as e:
            print(f"Error al subir los datos: {e}")
            # Deshacer la transacción en caso de error
            if self.conexion:
                self.conexion.rollback()
        
        finally:
            # Cerrar cursor y conexión
            if 'cursor' in locals():
                cursor.close()
            self._cerrar_conexion()

def principal():
    # Configuración de conexión para Docker Compose
    subidor = SubidorDeBaseDeDatos(
        host='172.29.0.2',     # IP del contenedor de base de datos
        usuario='scraperuser',    # Usuario proporcionado
        contrasena='scraperpass',  # Contraseña proporcionada
        base_de_datos='scraper_data'  # Nombre de la base de datos
    )

    # Ruta al archivo JSON con los datos scrapeados
    archivo_datos_scrapeados = 'src/expedientes.json'
    
    # Subir datos
    subidor.subir_expedientes(archivo_datos_scrapeados)

if __name__ == "__main__":
    principal()
