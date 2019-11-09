# WeatherScraper

Esta práctica de scraping se enmarca en las actividades de la asignatura "Tipología y ciclo de vida de los datos". llevada a cabo en el máster universitario de ciencia de datos impartido por la UOC.

El objetivo de la práctica es realizar web scraping de datos de estaciones meteorológicas cercanas a una localización geográfica, con el objetivo de realizar en un futuro, el mantenimiento predictivo de una instalación fotovoltáica.

Para poder ejecutar el script, es necesario tener instalados los siguientes paquetes de python:

* requests
* BeautifulSoup
* time
* datetime
* csv 

Tras la ejecución del script, se preguntará al usuario si desea iniciar un nuevo archivo de datos csv, o se desea continuar añadiendo datos al ya existente. Después se solicitará el número de ciclos horarios que se pretende capturar, una vez introducido este número de ciclos, el script capturará los datos cada hora y los registrará en el archivo meteo_data.csv, hasta completar el número de ciclos indicado.
