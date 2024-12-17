import os
import json
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    StaleElementReferenceException, 
    TimeoutException, 
    NoSuchElementException
)

def setup_driver():
    """
    Configura y retorna el driver de Selenium con opciones predeterminadas 
    para evitar problemas de ejecución en contenedores.
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def ensure_src_directory():
    """
    Crea el directorio 'src' si no existe para almacenar archivos de salida.
    
    Returns:
        str: Ruta al directorio 'src'
    """
    src_dir = os.path.join(os.getcwd(), 'src')
    os.makedirs(src_dir, exist_ok=True)
    return src_dir

def save_json_data(data, filename="expedientes.json"):
    """
    Guarda los datos extraídos en un archivo JSON dentro del directorio 'src'.
    
    Args:
        data (dict): Datos a guardar
        filename (str): Nombre del archivo de salida
    """
    src_dir = ensure_src_directory()
    filepath = os.path.join(src_dir, filename)
    
    # Leer datos existentes o iniciar lista vacía
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Agregar nuevos datos
    existing_data.append(data)

    # Guardar datos actualizados
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

def wait_for_element(driver, by, value, timeout=5):
    """
    Espera hasta que el elemento especificado esté presente y sea interactuable.
    
    Args:
        driver: Instancia del webdriver
        by: Método de localización del elemento
        value: Valor para localizar el elemento
        timeout: Tiempo máximo de espera
    
    Returns:
        WebElement: Elemento encontrado o None
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
    except Exception:
        return None

def buscar_parte(driver):
    """
    Realiza la búsqueda inicial en la página web con los filtros específicos.
    
    Args:
        driver: Instancia del webdriver de Selenium
    """
    url = "http://scw.pjn.gov.ar/scw/home.seam"
    driver.get(url)

    # Hacer clic en el tab 'porParte'
    tab = wait_for_element(driver, By.XPATH, '//*[@id="formPublica:porParte:header:inactive"]')
    if tab:
        tab.click()

    # Seleccionar "COM" en el <select> de jurisdicción
    jurisdiccion_select = wait_for_element(driver, By.ID, "formPublica:camaraPartes")
    if jurisdiccion_select:
        select = Select(jurisdiccion_select)
        select.select_by_value("10")

    # Escribir 'residuos' en el campo de búsqueda
    input_element = wait_for_element(driver, By.XPATH, '//*[@id="formPublica:nomIntervParte"]')
    if input_element:
        input_element.send_keys("residuos")

    # Pausar para resolver CAPTCHA manualmente
    input("Por favor, resuelve el CAPTCHA y presiona Enter...")

    # Hacer clic en el botón "Consultar"
    boton_consultar = wait_for_element(driver, By.ID, "formPublica:buscarPorParteButton")
    if boton_consultar:
        boton_consultar.click()

def hacer_click_siguiente(driver):
    """
    Intenta hacer clic en el botón 'Siguiente' manteniendo los selectores originales.
    
    Args:
        driver: Instancia del webdriver
    
    Returns:
        bool: True si se pudo ir a la siguiente página, False en caso contrario
    """
    try:
        boton_siguiente = driver.find_element(By.XPATH, '//*[@id="j_idt118:j_idt208:j_idt215"]')
        
        if boton_siguiente.is_displayed() and boton_siguiente.is_enabled():
            boton_siguiente.click()
            return True
        
        return False
    except Exception:
        return False

def hacer_click_expediente(driver):
    """
    Hace clic en el ícono del expediente utilizando la clase del ícono.
    
    Args:
        driver: Instancia del webdriver
    
    Returns:
        bool: True si se pudo hacer clic, False en caso contrario
    """
    try:
        icono_ver = driver.find_element(By.CLASS_NAME, "fa-eye")
        
        if icono_ver.is_displayed() and icono_ver.is_enabled():
            icono_ver.click()
            return True
        
        return False
    except Exception:
        return False

def extraer_expediente(driver):
    """
    Extrae datos generales (expediente, carátula, y dependencia) de la página web,
    incluyendo las fechas, tipos y detalles de la tabla, y los actores y demandados de la sección "Intervinientes".
    """
    try:
        # Diccionario para almacenar los datos extraídos
        datos = {}

        # Extraer expediente
        contenedor_expediente = driver.find_element(By.CLASS_NAME, "col-xs-10")
        datos["expediente"] = contenedor_expediente.find_element(By.TAG_NAME, "span").text.strip()

        # Extraer jurisdicción
        jurisdiccion_contenedor = driver.find_element(By.ID, "expediente:j_idt90:detailCamera")
        datos["jurisdiccion"] = jurisdiccion_contenedor.text.strip()

        # Extraer dependencia
        dependencia_contenedor = driver.find_element(By.ID, "expediente:j_idt90:detailDependencia")
        datos["dependencia"] = dependencia_contenedor.text.strip()

        # Extraer situación actual
        situacion_contenedor = driver.find_element(By.ID, "expediente:j_idt90:detailSituation")
        datos["situacion_actual"] = situacion_contenedor.text.strip()

        # Extraer carátula
        caratula_contenedor = driver.find_element(By.ID, "expediente:j_idt90:detailCover")
        datos["caratula"] = caratula_contenedor.text.strip()

        # Extraer datos de la tabla de movimientos
        try:
            tabla = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "expediente:action-table"))
            )
            filas = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#expediente\\:action-table tr"))
            )

            # Verificar si la tabla contiene filas (excluyendo encabezado)
            registros_tabla = []
            for fila in filas[1:]:
                celdas = fila.find_elements(By.TAG_NAME, "td")
                if len(celdas) >= 5:
                    registros_tabla.append({
                        "fecha": celdas[2].text.strip(),
                        "tipo": celdas[3].text.strip(),
                        "detalle": celdas[4].text.strip()
                    })
            datos["registros_tabla"] = registros_tabla
        except TimeoutException:
            datos["registros_tabla"] = []

        # Extraer datos de la sección "Intervinientes"
        intervinientes_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Intervinientes']"))
        )
        intervinientes_tab.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#expediente\\:participantsTable"))
        )

        actores, demandados = [], []
        filas = driver.find_elements(By.CSS_SELECTOR, "#expediente\\:participantsTable .rf-dt-r")
        for fila in filas:
            tipo = fila.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip().upper()
            nombre = fila.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()
            if "ACTOR" in tipo:
                actores.append(nombre)
            elif "DEMANDADO" in tipo:
                demandados.append(nombre)

        datos["actores"] = actores
        datos["demandados"] = demandados

        # Guardar los datos en un archivo JSON
        save_json_data(datos)

        # Confirmar éxito
        print(f"Expediente {datos['expediente']} extraído correctamente")

        return datos

    except Exception as e:
        print(f"Error al extraer los datos generales: {e}")
        return None



def volver_a_tabla(driver):
    """
    Hace clic en el botón de 'Volver' para regresar a la tabla de expedientes.
    
    Args:
        driver: Instancia del webdriver
    
    Returns:
        bool: True si se pudo volver, False en caso contrario
    """
    try:
        boton_volver = driver.find_element(By.CLASS_NAME, "btn-default")
        
        if boton_volver.is_displayed() and boton_volver.is_enabled():
            boton_volver.click()
            return True
        
        return False
    except Exception:
        return False

def navegar_y_extraer(driver):
    """
    Navega por las páginas de la tabla, hace clic en los expedientes y extrae información.
    
    Args:
        driver: Instancia del webdriver
    
    Returns:
        int: Total de expedientes extraídos
    """
    total_expedientes = 0

    while True:
        try:
            tabla = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table-striped"))
            )
            
            def procesar_tabla():
                nonlocal total_expedientes
                filas = driver.find_elements(By.TAG_NAME, "tr")[1:]
                
                for i in range(len(filas)):
                    try:
                        filas = driver.find_elements(By.TAG_NAME, "tr")[1:]
                        fila_actual = filas[i]
                        
                        try:
                            icono_ver = fila_actual.find_element(By.CLASS_NAME, "fa-eye")
                        except Exception:
                            continue
                        
                        driver.execute_script("arguments[0].click();", icono_ver)
                        
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "col-xs-10"))
                        )
                        
                        expediente = extraer_expediente(driver)
                        if expediente:
                            total_expedientes += 1

                        volver_a_tabla(driver)
                        
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "table-striped"))
                        )
                        
                    except StaleElementReferenceException:
                        continue
                    except Exception:
                        continue
            
            procesar_tabla()

        except Exception:
            break

        if not hacer_click_siguiente(driver):
            break

        time.sleep(2)
    
    return total_expedientes

def main():
    """
    Función principal que orquesta el proceso de scraping.
    """
    driver = setup_driver()

    try:
        buscar_parte(driver)
        total_expedientes = navegar_y_extraer(driver)
        print(f"Se extrajeron {total_expedientes} expedientes.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()