import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
pd.__version__

usuarioCUIT = '00000000000'
claveFiscal = 'contraseña'

espera = 2

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

driver.get('https://auth.afip.gob.ar/contribuyente_/login.xhtml')
time.sleep(espera)
driver.find_element(By.XPATH, '//*[@id="F1:username"]').send_keys(usuarioCUIT)
time.sleep(espera)
driver.find_element(By.XPATH, '//*[@id="F1:btnSiguiente"]').click()
time.sleep(espera)
driver.find_element(By.XPATH, '//*[@id="F1:password"]').send_keys(claveFiscal)
time.sleep(espera)
driver.find_element(By.XPATH, '//*[@id="F1:btnIngresar"]').click()
time.sleep(espera)
driver.find_element(By.XPATH, '//*[@id="serviciosMasUtilizados"]/div/div/div/div[1]/a').click()
time.sleep(espera)
driver.switch_to.window(driver.window_handles[1])
driver.find_element(By.XPATH, '//*[@id="contenido"]/form/table/tbody/tr[4]/td/input[2]').click()
time.sleep(espera)
driver.find_element(By.XPATH, '//*[@id="btn_gen_cmp"]/span[2]').click()
time.sleep(espera)
driver.find_element(By.XPATH, '//*[@id="puntodeventa"]/option[2]').click()
time.sleep(espera)
driver.find_element(By.XPATH, '//*[@id="contenido"]/form/input[2]').click()

df = pd.read_csv(r'..\Facturar.csv')

for index, row in df.iterrows():
    print(row['Concepto'], row['IVA'], row['Order Date'], row['Nombre y apellido'], row['Producto'], row['Precio'], row['Forma de pago'], row['Imprimir'])
    concepto = row['Concepto']
    iva = row['IVA']
    fecha = row['Order Date']
    nombre = row['Nombre y apellido']
    cuit = row['CUIT']
    producto = row['Producto']
    precio = row['Precio']
    fPago = row['Forma de pago']
    imprimir = row['Imprimir']
    
    time.sleep(1)
    #fecha
    driver.find_element(By.XPATH,'//*[@id="fc"]').clear()
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="fc"]').send_keys(fecha)
    time.sleep(1)

    if (concepto == 1):
        driver.find_element(By.XPATH, '//*[@id="idconcepto"]/option[2]').click() #Producto
    if (concepto == 2):
        driver.find_element(By.XPATH, '//*[@id="idconcepto"]/option[3]').click() #servicio
    if (concepto == 3):
        driver.find_element(By.XPATH, '//*[@id="idconcepto"]/option[4]').click() #Producto y servicio
    
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="contenido"]/form/input[2]').click()

    time.sleep(2)
    
    if(iva == 1):#Consumidor Final
        driver.find_element(By.XPATH,'//*[@id="idivareceptor"]/option[4]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="idtipodocreceptor"]/option[7]').click()#DNI
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="razonsocialreceptor"]').send_keys(nombre)

    if(iva == 2):#Responsable Inscripto
        driver.find_element(By.XPATH,'//*[@id="idivareceptor"]/option[2]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="nrodocreceptor"]').send_keys(cuit)
        
    
    if(iva == 3):#Sujeto Exento
        driver.find_element(By.XPATH,'//*[@id="idivareceptor"]/option[3]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="nrodocreceptor"]').send_keys(cuit)

    time.sleep(1)

    if (fPago == 1): #Cuenta Corriente
        driver.find_element(By.XPATH,'//*[@id="formadepago4"]').click()
    if (fPago == 2): #Contado
        driver.find_element(By.XPATH,'//*[@id="formadepago1"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="formulario"]/input[2]').click()
    time.sleep(1)


    driver.find_element(By.XPATH,'//*[@id="detalle_descripcion1"]').send_keys(producto)
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="detalle_precio1"]').send_keys(precio)
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="contenido"]/form/input[8]').click()
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="btngenerar"]').click()
    time.sleep(1)

    #enter
    driver.switch_to.alert.accept()
    time.sleep(1)

    if (imprimir == 1):
        driver.find_element(By.XPATH,'//*[@id="botones_comprobante"]/input').click() #Imprimir
        time.sleep(1)
    
    driver.find_element(By.XPATH,'//*[@id="contenido"]/table/tbody/tr[2]/td/input').click() #menu principal
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="btn_gen_cmp"]/span[2]').click() #generar comprobante
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="puntodeventa"]/option[2]').click() #cardiel 
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="contenido"]/form/input[2]').click() #continuar