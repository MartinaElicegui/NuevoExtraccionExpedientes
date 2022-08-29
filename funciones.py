from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import *
from easygui import *
from selenium import webdriver
from random import randint
from time import sleep
import csv
import inspect
import os
import re


# Genera una instancia del navegador automatizado
# Argumentos: -
# Devuelve: driver
def generarDriver():
    rutaDriver = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(rutaDriver, chrome_options=Options())
    Options().add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/59.0.3071.115 Safari/537.36")
    return driver

# Loguea al profesional dentro del SISFE
# Argumentos: driver
# Devuelve: -
def loguearProfesional(driver):
    driver.maximize_window()
    infoLogueo = leerInformacionLogin()
    ingresarAurl(driver)
    cargarDatosLogin(driver, infoLogueo)
    msgbox("Complete el captcha y presione una tecla para continuar")
    navegar(driver)

# Lee la información necesaria para loguearse de un archivo csv
# Argumentos: -
# Devuelve: [circunscripcion, colegio, matricula, contraseña] -> una lista de 4 strings
def leerInformacionLogin():
    informacion = open("datos.csv", "r", encoding="latin1")

    linea = informacion.readline()

    datosIngreso = linea.split(',')
    circunscripcion = datosIngreso[0]
    colegio = datosIngreso[1]
    matricula = datosIngreso[2]
    contraseña = datosIngreso[3]

    return [circunscripcion, colegio, matricula, contraseña]

# Ingresa a la página del login
# Argumentos: driver
# Devuelve: -
def ingresarAurl(driver):
    driver.get('https://sisfe.justiciasantafe.gov.ar/login-matriculado')

# Carga la información en los elementos HTML del login
# Argumentos: driver - infoLogueo (la lista de 4 strings que devuelve la función "leerInformacionLogin()")
# Devuelve: -
def cargarDatosLogin(driver, infoLogueo):
    droplistCircunscripcion = encontrarElemento(driver, "circunscripcion")
    droplistCircunscripcion.send_keys(infoLogueo[0])
    droplistColegio = encontrarElemento(driver, "colegio")
    droplistColegio.send_keys(infoLogueo[1])
    textfieldMatricula = encontrarElemento(driver, "matricula")
    textfieldMatricula.send_keys(infoLogueo[2])
    textfieldContraseña = encontrarElemento(driver, "contraseña")
    textfieldContraseña.send_keys(infoLogueo[3])

# Busca elementos e introduce esperas para reducir errores
# Argumentos: driver - nombreElemento (string con el nombre del elemento a buscar)
# Devuelve: elemento (html)
def encontrarElemento(driver, nombreElemento):
    if (nombreElemento == "circunscripcion"):
        droplistCircunscripcion = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//select[@id="circunscripcion"]'))
        )
        return droplistCircunscripcion
    if (nombreElemento == "colegio"):
        droplistColegio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//select[@id="colegio"]'))
        )
        return droplistColegio
    if (nombreElemento == "matricula"):
        textfieldMatricula = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@id="matricula"]'))
        )
        return textfieldMatricula
    if (nombreElemento == "contraseña"):
        textfieldContraseña = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@id="password"]'))
        )
        return textfieldContraseña
    if (nombreElemento == "botonIngresar"):
        botonIngresar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@id="ingresar"]'))
        )
        return botonIngresar
    if (nombreElemento == "CUIJ"):
        textfieldCUIJ = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="cuij"]'))
        )
        return textfieldCUIJ
    if (nombreElemento == "efectuarBusqueda"):
        botonEfectuarBusqueda = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@id="efectuarBusqueda"]'))
        )
        return botonEfectuarBusqueda
    if (nombreElemento == "linkCUIJ"):
        linkCUIJ = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@href,"/detalle-expediente/")]'))
        )
        return linkCUIJ
    if (nombreElemento == "botonPasarPagina"):
        # botonPasarPagina = driver.find_element(
        #         By.XPATH, '//li[contains(@class, "page-item next-item")]'
        #     )
        botonPasarPagina = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//li[contains(@class, "page-item next-item")]'))
        )
        return botonPasarPagina
    if (nombreElemento == "botonDesplegar"):
        botonDesplegar = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//form[@class="ng-valid ng-dirty ng-touched"]//div[@class="card-header"]//i'))
        )
        return botonDesplegar

# Navega a través del sitio para llegar a la página deseada
# Argumentos: driver
# Devuelve: si lo llama la función loguear profesional, nada.
#           si lo llama la función leerInformaciónExpediente, [fecha, textoAdjunto] (la lista de dos elementos que devuelve la función "extraerSegundoAdjunto")
def navegar(driver):
    llamador = inspect.stack()[1][3]

    if (llamador == "loguearProfesional"):
        botonIngresar = encontrarElemento(driver, "botonIngresar")
        botonIngresar.click()
    # if (llamador == "leerInformacionExpediente"):
    #     #sleep(2)
    #     resultado = extraerSegundoAdjunto(driver)
    #     return resultado 

# Extrae el segundo archivo (que está en otra página)
# Argumentos: driver
# Devuelve: [fecha, textoAdjunto] -> una lista de dos elementos tipo string
def extraerSegundoAdjunto(driver):
    #sleep(1)
    fecha = driver.find_element_by_xpath("//table//tbody//td[1]/span/span").text
    #print("FECHA: ", fecha)
    #print("TIPO DE DATO FECHA: ", type(fecha))
    textoAdjunto = driver.find_element_by_xpath("//table//tbody//td[2]/span/span").text
    #print("TEXTO ADJUNTO: ", textoAdjunto)
    #print("TIPO DE TEXTO ADJUNTO: ", type(textoAdjunto))
    # archivoAdjunto = driver.find_element_by_xpath("//table//tbody//td[4]/span/button/i")
    # archivoAdjunto = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//table//tbody//td[4]/span/button")))
    # archivoAdjunto = driver.find_element_by_xpath("//table//tbody//td[4]/span/button/i")
    archivoAdjunto = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//table//tbody//td[4]/span/button/i'))
        )
    archivoAdjunto.click()
    #sleep(3)
    paginaAnterior(driver)
    return [fecha, textoAdjunto]

# Vuelve a la página anterior que se había visitado.
# Argumentos: driver
# Devuelve: -
def paginaAnterior(driver):
    driver.execute_script("window.history.go(-1)")
    # driver.back()

# Busca el expediente dentro del buscador por CUIJ
# Argumentos: driver
# Devuelve: -
def buscarExpediente(driver):
    cuijs = leerCUIJ()
    cargarCUIJ(driver, cuijs)
    navegar(driver)

# Lee el archivo y agrupa los CUIJS a buscar
# Argumentos: -
# Devuelve: class '_io.TextIOWrapper' de cuijs
def leerCUIJ():
    cuijs = []
    listaCUIJs = open("cuijs.csv", "r", encoding="latin1")
    for fila in listaCUIJs:
        cuijs.append(fila)
    return cuijs

# Carga el CUIJ y efectúa la búsqueda
# Argumentos: driver, cuijs (lista de strings devuelta por la función "leerCUIJ()")
# Devuelve: -
def cargarCUIJ(driver, cuijs): 
    scrollArriba(driver)
    # desplegarCuadroBusqueda(driver)
    textfieldCUIJ = encontrarElemento(driver, "CUIJ")
    # CUIJ con 39 registros (con paginación): 21-26361795-6. Adjuntos: 25 P1 - 22 P2 (47)
    # CUIJ con 10 registros (sin paginación): 21-26362099-9. Adjuntos: 5 A1 - 5 A2
    # CUIJ con 54 registros (con paginación): 21-05016495-8. Adjuntos: 36 A1 - 
    textfieldCUIJ.send_keys("21-26362099-9")
    botonEfectuarBusqueda = encontrarElemento(driver, "efectuarBusqueda")
    botonEfectuarBusqueda.click()
    linkCUIJ = encontrarElemento(driver, "linkCUIJ")
    linkCUIJ.click()
    extraerInformacion(driver)

# Intenta encontrar el cuadro de búsqueda
# Argumentos: driver
# Devuelve: -
def desplegarCuadroBusqueda(driver):
    try:
        botonDesplegarBusqueda = encontrarElemento(driver, "botonDesplegar")
        botonDesplegarBusqueda.click()
    except:
        paginaAnterior(driver)
        desplegarCuadroBusqueda(driver)

# Extrae y guarda la información recolectada
# Argumentos: driver
# Devuelve: -
def extraerInformacion(driver):
    #sleep(5)
    filas = WebDriverWait(driver,30).until(EC.visibility_of_all_elements_located((By.XPATH, "//table/tbody/tr")))
    # filas = driver.find_elements_by_xpath("//table/tbody/tr")
    numeroFilas = len(filas)
    leerInformacionExpediente(driver, numeroFilas)
    # pasarPagina(driver)

# Toma la información correspondiente a los movimientos del expediente
# Argumentos: driver, númerodeFilas (integer) -> calculado en la función “extraerInformación”
# Devuelve: -
def leerInformacionExpediente(driver, numeroFilas):
    #sleep(5)
    print("Se han encontrado: ", numeroFilas, " filas")
    for i in range(1,numeroFilas+1):
        print("Entra al for")
        print ("Vuelta nro: ", i)
        try:
            tipoMovimiento1 = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]//td[1]//i"))) 
            tipoMovimiento1 = tipoMovimiento1.get_attribute('class')
        # tipoMovimiento1 = driver.find_element(
        #     By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]//td[1]//i").get_attribute('class')
            tipoMov1 = identificarMovimiento(tipoMovimiento1)
        except:
            tipoMov1 = "sinMov1"
        try:
            tipoMovimiento2 = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[2]//i"))) 

            # tipoMovimiento2 = driver.find_element(
            #     By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[2]//i").get_attribute('class')
            tipoMovimiento2 = tipoMovimiento2.get_attribute('class')
            tipoMov2 = identificarMovimiento(tipoMovimiento2)
        except:
            tipoMov2 = "sinMov2"
        try:
            # fecha = driver.find_element(
            #     By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[3]/span/span").text
            fecha = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[3]/span/span"))) 
            fecha = fecha.text
        except:
            fecha = "sinFecha"
        try:
            # novedad = driver.find_element(
            #     By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[4]/span/span").text
            novedad = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[4]/span/span"))) 
            novedad = novedad.text
        except:
            novedad = "sinNovedad"
        try:
            # observacion = driver.find_element(
            #     By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[5]/span/span").text
            observacion = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[4]/span/span"))) 
            observacion = observacion.text
            observacion = observacion.replace("\n", " // ")
        except:
            observacion = "sinObservacion"
        try:
            scrollSuave(driver)
            scrollSuave(driver)
            # adjunto1 = driver.find_element(
            #     By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[6]//button/i")
            adjunto1 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[6]//button/i"))
                    )    
            adjunto1.click()
            #sleep(5)
        except:
            pass
        try:
            scrollSuave(driver)
            scrollSuave(driver)
            # adjunto2 = driver.find_element(
            #     By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[8]//button/i")
            adjunto2 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[8]//button/i"))
                    )    
            adjunto2.click()
            #sleep(3)
            
            textoYfechaAdjunto = navegar(driver)
        except:
            pass
        guardarInformacion(tipoMov1, tipoMov2, fecha, novedad, observacion)

# Evalúa la necesidad (o no) de pasar página
# Argumentos: driver
# Devuelve: -
def pasarPagina(driver):
    scrollSuave(driver)
    #sleep(5)
    try:
        botonPasarPagina = encontrarElemento(driver, "botonPasarPagina")
        claseBotonPasarPagina = botonPasarPagina.get_attribute('class')
        claseSinEspacios = claseBotonPasarPagina.strip()

        claseEsperada = "page-item next-item enabled"
        print("La clase encontrada es: ", claseSinEspacios,"con longitud :", len(claseSinEspacios))
        print("La clase esperada es: ", claseEsperada, "con longitud :", len(claseEsperada))
        if (claseSinEspacios == claseEsperada):
            msgbox('Acepte para pasar a la siguiente página.')
            botonPasarPagina.click()
            #sleep(5)
            extraerInformacion(driver)
    except:
        print("No se ha encontrado otra página.")
        pass

# Utiliza la lista de referencias para interpretar el ícono encontrado
# Argumentos: movimiento (string) -> generado por la función "leerInformacionExpediente"
# Devuelve: mov (string) -> el resultado de la interpretación del ícono
def identificarMovimiento(movimiento):
    result1 = movimiento.find("file")
    result2 = movimiento.find("gavel")
    result3 = movimiento.find("shield")
    result4 = movimiento.find("user-check")

    encontrado = 15

    if (result1 == encontrado):
        mov = "Escrito"
    if (result2 == encontrado):
        mov = "Resolución/Sentencia"
    if (result3 == encontrado):
        mov = "Trámite"
    if (result4 == encontrado):
        mov = "Notificaciones con firma digital"
    return mov

# Guarda la información recolectada
# Argumentos: tipoMov1, tipoMov2, fecha, novedad, observacion -> generados por la función "leerInformacionExpediente"
# Devuelve: -
def guardarInformacion(tipoMov1, tipoMov2, fecha, novedad, observacion):
    with open('datosExtraidos.csv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter = ',', lineterminator='\n')
        writer.writerow([tipoMov1, tipoMov2, fecha, novedad, observacion])

def scroll(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

def scrollSuave(driver):
    driver.execute_script("window.scrollTo(0, window.scrollY + 300)")

def scrollArriba(driver):
    driver.execute_script("window.scrollBy(0,0)","")

# def scrollIntoView:
#     element.scrollIntoView({block: "end"});

def contarArchivosADescargar(driver):
    # archivos = driver.find_elements_by_xpath('//i[@class ="color-verde fa-paperclip fas"]')
    # archivos = driver.find_elements_by_class_name('color-verde fa-paperclip fas')
    archivos = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//i[@class ="color-verde fa-paperclip fas"]'))) 
    print ("SE DEBEN DESCARGAR ", len(archivos), " archivos.")

def contarArchivosDescargados():
    img_folder_path = r"C:\Users\pasros01\Downloads"
    dirListing = os.listdir(img_folder_path)
    print("--------Estos son los archivos descargados: ")
    dirListing.remove('desktop.ini')
    for file in dirListing:
        print(file)
    print("*************La cantidad de archivos descargados es: ", len(dirListing))