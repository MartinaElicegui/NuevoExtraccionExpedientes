import sys
from funcionesDos import *
from easygui import *

def main():
    driver = generarDriver()
    ingresarAurl(driver)
    msgbox("Presione una tecla para terminar")
    
if __name__ == "__main__":
    sys.exit(main())