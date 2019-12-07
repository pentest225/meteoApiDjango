from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import json
from django.http import JsonResponse


url = 'https://www.tameteo.com/meteo_Abidjan-Afrique-Cote+dIvoire-Abidjan-DIAP-1-8908.html'
# Create your views here.



def getmeteo(url):


    req = requests.get(url)

    print(req.status_code)

    html_doc = req.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    divbloc = soup.find('span', attrs={ 'class':'columnas zona-contenido padding-top-doble horas-sol-lunas' })

    print(len(divbloc))

    principale = divbloc.find('table', attrs={ 'class':'tabla-horas' })

    table = principale.find_all('tr')
    i = 1
    data = []
    for it in table:
        meteo = {}
        if i % 2 == 0:
            #print(it.text)
            hora = it.find('span', attrs={'class':'hora'})
            temp = it.find('td', attrs={'class':'temperatura changeUnitT'})
            description = it.find('td', attrs={'class':'descripcion'})
            vent = it.find('span', attrs={'class':'datos-viento'})
            descvent = vent.find('strong')

            heure = hora.text
            temperature = temp.text
            descripcion = description.text
            directionvend = vent.text

            meteo['heure'] = heure
            meteo['temperature'] = temperature
            meteo['directionvend'] = directionvend
            meteo['descripcion'] = descripcion

            data.append(meteo)

        else:

            pass

        i += 1

    return data


def meteo(request):
    datas = getmeteo(url)
    
    return JsonResponse(data=datas, safe=False)

