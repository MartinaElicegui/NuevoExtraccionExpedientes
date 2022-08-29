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
    try:
        rutaDriver = os.path.join(os.getcwd(), "chromedriver")
        driver = webdriver.Chrome(rutaDriver, chrome_options=Options())
        Options().add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/59.0.3071.115 Safari/537.36")
        return driver
    except:
        print("Ha ocurrido un error en la función generarDriver()")

# Ingresa a la página del login
# Argumentos: driver
# Devuelve: -
def ingresarAurl(driver):
    try:
        driver.get('https://sisfe.justiciasantafe.gov.ar/login-matriculado')
        driver.maximize_window()
    except:
        print("Ha ocurrido un error en la función ingresarAurl()")