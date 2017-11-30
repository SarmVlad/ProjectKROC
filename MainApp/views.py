from django.db.models.functions.datetime import datetime
from django.shortcuts import render
from django.http import Http404, HttpResponse
from MainApp import models
from PIL import Image
import requests
from django.http import JsonResponse
import json
import os


def index(request, year, month, day, city, method="json"):

    #True it's man, false - woman

    if models.request.objects.all().filter(date=year + '-' + month + '-' + day, city=city).count() == 0:
        
        # Начало работы с API
        App_Id = "cd4ae38185273442f9a802c3b3a02665"
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'q': city, 'cnt': '16', 'units': 'metric', 'lang': 'ru', 'APPID': App_Id})
        data = res.json()
        data_list = []
        for a in data['list']:
            day_weather = {'temp': a['main']['temp'], 'humidity': a['main']['humidity'], 'wind': a['wind']['speed']}
            data_list.append(day_weather)

        # Получаем данные для запрашиваемого дня
        delta_date = (datetime.date(datetime(int(year), int(month), int(day))) - datetime.now().date()).days
        requested_temp = data_list[delta_date]['temp']
        requested_humidity = data_list[delta_date]['humidity']
        requested_wind = data_list[delta_date]['wind']
        # Конец API

        path_m = 'results/res-man' + '_' + year + '_' + month + '_' + day + '-' + city + '.png'
        path_f = 'results/res-woman' + '_' + year + '_' + month + '_' + day + '-' + city + '.png'
        Scotcher(True, requested_temp, requested_humidity, requested_wind).save( os.getcwd() + '/MainApp/static/' + path_m)
        Scotcher(False, requested_temp, requested_humidity, requested_wind).save(os.getcwd() + '/MainApp/static/' + path_f)
        json_dict = {'url': { 'man' : 'static/results/res-man' + '_' + year + '_' + month + '_' + day + '-' + city + '.png',
                              'woman' : 'static/results/res-woman' + '_' + year + '_' + month + '_' + day + '-' + city + '.png'},
                     'data': data_list}
        models.request.objects.create(date=year + '-' + month + '-' + day, city=city, json=json.dumps(json_dict),res_file_name_m=path_m, res_file_name_f=path_f)

        if method == "html":
            context = {
                'res_path_m': path_m,
                'res_path_f': path_f,
            }
            return render(request, "index.html", context)
        response = JsonResponse(json_dict)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        cash = models.request.objects.get(date=year + '-' + month + '-' + day, city=city)
        if method == "html":
            context = {
                'res_path_m': cash.res_file_name_m,
                'res_path_f': cash.res_file_name_f,
            }
            return render(request, "index.html", context)
        response = HttpResponse(cash.json, content_type="application/json")
        response['Access-Control-Allow-Origin'] = '*'
        return response


# Функция по составлению человечка
def Scotcher(man, temp, humidity, wind):
    Garb = models.garb.objects
    if temp < 0:
        if man:
            hat = Garb.get(ident=1)
        else:
            hat = Garb.get(ident=2)
    else:
        if man:
            hat = Garb.get(ident=3)
        else:
            hat = Garb.get(ident=2)
    pants = Garb.get(ident=4)
    tshirt = Garb.get(ident=5)
    vest = Garb.get(ident=6)

    path = os.getcwd() + "/MainApp"
    man = Image.open(path + '/static/source/' + 'man.png')  # Берём скелет

    # Загружаем одежду
    img_hat = Image.open(path + '/static/source/' + hat.file_name)
    img_pants = Image.open(path + '/static/source/' + pants.file_name)
    img_tshirt = Image.open(path + '/static/source/' + tshirt.file_name)
    img_vest = Image.open(path + '/static/source/' + vest.file_name)

    # Склеиваем
    man.paste(img_hat, (hat.cord_x, hat.cord_y), img_hat)
    man.paste(img_pants, (pants.cord_x, pants.cord_y), img_pants)
    man.paste(img_tshirt, (tshirt.cord_x, tshirt.cord_y), img_tshirt)
    man.paste(img_vest, (vest.cord_x, vest.cord_y), img_vest)
    return man