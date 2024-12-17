import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime

import mysql.connector
from mysql.connector import Error

# Configuración de logging para tener un seguimiento detallado de las operaciones
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ScraperDatabaseError(Exception):
    """Excepción personalizada para manejar errores específicos de la base de datos."""
    pass

class SubidorDeBaseDeDatos:
    """
    Clase para subir datos scrapeados a una base de datos MySQL.
    
    Gestiona la conexión, inserción de datos y manejo de errores durante 
    el proceso de transferencia de información desde archivos JSON a MySQL.
    """

    def __init__(self, config: Dict[str, str]):
        """
        Inicializa la configuración de conexión a la base de datos.
        
        :param config: Diccionario con configuraciones de conexión
        :type config: Dict[str, str]
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.conexion = None

    def _conectar(self) -> None:
        """
        Establece una conexión segura con la base de datos MySQL.
        
        :raises ScraperDatabaseError: Si no se puede establecer la conexión
        """
        try:
            self.conexion = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['usuario'],
                password=self.config['contrasena'],
                database=self.config['base_de_datos']
            )
            if self.conexion.is_connected():
                self.logger.info("Conexión exitosa a la base de datos")
        except Error as e:
            error_msg = f"Error al conectar a la base de datos MySQL: {e}"
            self.logger.error(error_msg)
            raise ScraperDatabaseError(error_msg)

    def _cerrar_conexion(self) -> None:
        """Cierra de manera segura la conexión a la base de datos."""
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            self.logger.info("Conexión a la base de datos cerrada")

    def _validar_datos(self, datos: List[Dict]) -> bool:
        """
        Valida la estructura básica de los datos scrapeados.
        
        :param datos: Lista de diccionarios con datos scrapeados
        :return: True si los datos son válidos, False en caso contrario
        """
        if not datos:
            self.logger.warning("No hay datos para procesar")
            return False
        
        campos_requeridos = ['expediente', 'jurisdiccion', 'dependencia']
        for caso in datos:
            if not all(campo in caso for campo in campos_requeridos):
                self.logger.error(f"Datos incompletos: {caso}")
                return False
        
        return True

    def limpiar_fecha(self, fecha: Optional[str]) -> Optional[datetime]:
        """
        Convierte y limpia el texto de fecha a un objeto datetime.
        
        :param fecha: Cadena de texto con la fecha
        :return: Objeto datetime o None si no se puede convertir
        """
        if not fecha:
            return None
        
        try:
            # Eliminar texto adicional y convertir a datetime
            fecha_limpia = fecha.replace('Fecha:', '').strip()
            return datetime.strptime(fecha_limpia, '%d/%m/%Y').date()
        except ValueError:
            self.logger.warning(f"No se pudo convertir la fecha: {fecha}")
            return None

    def subir_expedientes(self, archivo_datos_scrapeados: str) -> None:
        """
        Sube los datos de expedientes desde un archivo JSON a la base de datos.
        
        :param archivo_datos_scrapeados: Ruta al archivo JSON con datos
        :raises ScraperDatabaseError: Si ocurre un error durante la subida de datos
        """
        try:
            # Leer y validar datos
            with open(archivo_datos_scrapeados, 'r', encoding='utf-8') as archivo:
                datos_scrapeados = json.load(archivo)
            
            if not self._validar_datos(datos_scrapeados):
                raise ScraperDatabaseError("Datos inválidos para subir")

            # Establecer conexión
            self._conectar()
            cursor = self.conexion.cursor()

            # Procesar cada caso
            for caso in datos_scrapeados:
                # Inserción de expediente principal
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

                # Inserción de movimientos
                if caso.get('registros_tabla'):
                    consulta_movimientos = """
                    INSERT INTO movimientos 
                    (expediente_id, fecha, tipo, detalle) 
                    VALUES (%s, %s, %s, %s)
                    """
                    valores_movimientos = [
                        (expediente_id, 
                         self.limpiar_fecha(registro['fecha']), 
                         registro['tipo'], 
                         registro['detalle']) 
                        for registro in caso.get('registros_tabla', [])
                    ]
                    cursor.executemany(consulta_movimientos, valores_movimientos)

                # Inserción de participantes
                consulta_participantes = """
                INSERT INTO participantes 
                (expediente_id, tipo, nombre) 
                VALUES (%s, %s, %s)
                """
                valores_participantes = (
                    [(expediente_id, 'ACTOR', actor) for actor in caso.get('actores', [])] +
                    [(expediente_id, 'DEMANDADO', demandado) for demandado in caso.get('demandados', [])]
                )
                
                if valores_participantes:
                    cursor.executemany(consulta_participantes, valores_participantes)

            # Confirmar transacción
            self.conexion.commit()
            self.logger.info("¡Datos subidos exitosamente!")

            # Eliminar archivo después de subida exitosa
            self._eliminar_archivo(archivo_datos_scrapeados)

        except (Error, ScraperDatabaseError) as e:
            self.logger.error(f"Error al subir los datos: {e}")
            if self.conexion:
                self.conexion.rollback()
            raise
        
        finally:
            # Cerrar cursor y conexión
            if 'cursor' in locals():
                cursor.close()
            self._cerrar_conexion()

    def _eliminar_archivo(self, ruta_archivo: str) -> None:
        """
        Elimina el archivo de forma segura.
        
        :param ruta_archivo: Ruta completa del archivo a eliminar
        """
        try:
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                self.logger.info(f"Archivo {ruta_archivo} eliminado exitosamente")
        except OSError as e:
            self.logger.error(f"Error al eliminar el archivo: {e}")

def main():
    """
    Función principal para ejecutar la subida de datos.
    Configuración centralizada y manejo de errores.
    """
    # Configuración de conexión 
    config_db = {
        'host': '172.29.0.2',
        'usuario': 'scraperuser',
        'contrasena': 'scraperpass',
        'base_de_datos': 'scraper_data'
    }

    try:
        # Ruta al archivo JSON con los datos scrapeados
        archivo_datos = 'src/expedientes.json'
        
        # Instanciar y ejecutar subidor
        subidor = SubidorDeBaseDeDatos(config_db)
        subidor.subir_expedientes(archivo_datos)

    except ScraperDatabaseError as e:
        logging.error(f"Error en el proceso de subida: {e}")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()