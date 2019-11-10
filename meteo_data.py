import requests
from bs4 import BeautifulSoup
import time
from datetime import date
from datetime import datetime
import datetime
import csv 


######################
# Función de captura #
######################

def captura():
    
    page_olesa = requests.get("https://www.meteoclimatic.net/perfil/ESCAT0800000008640A")
    soup_olesa = BeautifulSoup(page_olesa.content)

    page_vacarisses = requests.get("https://www.meteoclimatic.net/perfil/ESCAT0800000008233A")
    soup_vacarisses = BeautifulSoup(page_vacarisses.content)
    
    #Buscamos los datos de interés que en la página se encuentran en el 'td' de clase "dadesactuals". 
    #Seleccionamos todos los datos menos el último, ya que los días de sequía no nos interesan.
    dades_olesa = soup_olesa.find_all('td', class_="dadesactuals")[0:5]
    dades_vacarisses = soup_vacarisses.find_all('td', class_="dadesactuals")[0:6]

    #Generamos los vectores para almacenar los datos.
    meteo_dat_olesa = []
    meteo_dat_vacarisses = []

    #Almacenamos los strings en los vectores de datos.
    for elem in dades_olesa:
        meteo_dat_olesa.append(elem.get_text())
    for elem in dades_vacarisses:
        meteo_dat_vacarisses.append(elem.get_text()) 

    #Añadimos dos posiciones más a la lista ya que la dirección del viendo se descompone en dos variables.
    meteo_dat_olesa.insert(2,None)
    meteo_dat_vacarisses.insert(2,None)

    #Modificamos ahora cada uno de los strings para convertirlos en datos numéricos.
    meteo_dat_olesa[0] = float(meteo_dat_olesa[0][:4])
    meteo_dat_vacarisses[0] = float(meteo_dat_vacarisses[0][:4])
    meteo_dat_olesa[1] = int(meteo_dat_olesa[1][:2])
    meteo_dat_vacarisses[1] = int(meteo_dat_vacarisses[1][:2])

    #En la dirección del viento, el el segundo char aparece como \xa0 (espacio vacío)#
    #por ejemplo en N (N\xa0), este espacio vacío se corresponde con el caracter chr(160)#
    if meteo_dat_olesa[3][1:2] == chr(160):
        meteo_dat_olesa[2] = int(meteo_dat_olesa[3][3:4])
    elif meteo_dat_olesa[3][2:3] == chr(160):
        meteo_dat_olesa[2] = int(meteo_dat_olesa[3][4:5])
    else:
        meteo_dat_olesa[2] = int(meteo_dat_olesa[3][5:6])

    if meteo_dat_vacarisses[3][1:2] == chr(160):
        meteo_dat_vacarisses[2] = int(meteo_dat_vacarisses[3][3:4])
    elif meteo_dat_vacarisses[3][2:3] == chr(160):
        meteo_dat_vacarisses[2] = int(meteo_dat_vacarisses[3][4:5])
    else:
        meteo_dat_vacarisses[2] = int(meteo_dat_vacarisses[3][5:6])

    #En la dirección del viento, el el segundo char aparece como \xa0 (espacio vacío)#
    #por ejemplo en N (N\xa0), este espacio vacío se corresponde con el caracter chr(160)#
    if meteo_dat_olesa[3][1:2] == chr(160):
        meteo_dat_olesa[3] = meteo_dat_olesa[3][0:1]
    elif meteo_dat_olesa[3][2:3] == chr(160):
        meteo_dat_olesa[3] = meteo_dat_olesa[3][0:2]
    else:
        meteo_dat_olesa[3] = meteo_dat_olesa[3][:3]
    if meteo_dat_vacarisses[3][1:2] == chr(160):
        meteo_dat_vacarisses[3] = meteo_dat_vacarisses[3][0:1]
    elif meteo_dat_olesa[3][2:3] == chr(160):
        meteo_dat_vacarisses[3] = meteo_dat_vacarisses[3][0:2]
    else:
        meteo_dat_vacarisses[3] = meteo_dat_vacarisses[3][:3]
    meteo_dat_olesa[4] = int(meteo_dat_olesa[4][:4])
    meteo_dat_vacarisses[4] = int(meteo_dat_vacarisses[4][:4])
    meteo_dat_olesa[5] = float(meteo_dat_olesa[5][:3])
    if meteo_dat_vacarisses[5][2:3] == 'W':
        meteo_dat_vacarisses[5] = int(meteo_dat_vacarisses[5][:1])
    else:
        meteo_dat_vacarisses[5] = int(meteo_dat_vacarisses[5][:3])
    meteo_dat_vacarisses[6] = float(meteo_dat_vacarisses[6][:3])

    return meteo_dat_olesa + meteo_dat_vacarisses


####################
#  Programa (main) #
####################

#Creación listado de atributos del csv.
names = ['dia', 'hora', 'temp_olesa', '%_hum_olesa', 'wind_speed_olesa', 'dir_wind_speed_olesa', 'pressure_olesa', 'rain_olesa',
         'temp_vacarisses', '%_hum_vacarisses', 'wind_speed_vacarisses', 'dir_wind_speed_vacarisses', 'pressure_vacarisses',
         'radiation_vacarisses', 'rain_vacarisses']

#Creación del archivo csv. Se consulta al usuario si quiere inicializarlo, o seguir añadiendo datos.
sn = str(input("¿Desea inicializar el archivo CSV de captura de datos s/n? "))

if sn == 's':
    csvsalida = open('meteo_data.csv', 'w', newline='')
    salida = csv.writer(csvsalida)
    salida.writerow(names)
    del salida
    csvsalida.close()
else:
    pass

#Consulta al usuario sobre el número de ciclos horarios en los que quiere que se registren los datos.
ciclos = int(input("¿Durante cuántas horas quiere que se registren los datos? "))

#Abrimos de nuevo el archivo csv para continuar archivando datos de los nuevos ciclos horarios.
csvsalida = open('meteo_data.csv', 'a', newline='')
salida = csv.writer(csvsalida)

#En cada ciclo realizaremos una lectura en las estaciones.
for i in range(ciclos):
    #Unimos los listados de fecha y hora junto con los datos obtenidos de las estaciones mediante la función capture().
    data_register = [datetime.date.today(), datetime.datetime.now().hour] + captura()
    print(data_register)
    salida.writerow(data_register)
    #Con time.sleep aplazamos cada lectura 1 hora (3600 segundos).
    time.sleep(3600)

del salida
csvsalida.close()

