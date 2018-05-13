# -*- coding: utf-8 -*-
from django.db.models.functions.datetime import datetime
from django.shortcuts import render
from django.http import Http404, HttpResponse
from MainApp import models
from PIL import Image
import requests
from django.http import JsonResponse
import json
import os
from django.utils import timezone
import pytz


def index(request, year, month, day, lat, lon, method="json"):

    #True it's man, false - woman

    if models.request.objects.all().filter(date=year + '-' + month + '-' + day, lat=lat, lon=lon).count() > 0:

        cash = models.request.objects.get(date=year + '-' + month + '-' + day, lat=lat, lon=lon)
        #Update every 3 hours
        if (timezone.now() - datetime(cash.request_date.year, cash.request_date.month, cash.request_date.day,
                                      cash.request_date.hour, cash.request_date.minute, cash.request_date.second,
                                      tzinfo=pytz.UTC)).seconds < 10800:

            if method == "html":
                context = {
                    'res_path_m': cash.res_file_name_m,
                    'res_path_f': cash.res_file_name_f,
                }
                return render(request, "index.html", context)
            response = HttpResponse(cash.json, content_type="application/json")
            response['Access-Control-Allow-Origin'] = '*'
            return response

        else:
            if os.path.isfile(os.getcwd() + '/MainApp/static/' + cash.res_file_name_f):
                os.remove(os.getcwd() + '/MainApp/static/' + cash.res_file_name_f)
            if os.path.isfile(os.getcwd() + '/MainApp/static/' + cash.res_file_name_m):
                os.remove(os.getcwd() + '/MainApp/static/' + cash.res_file_name_m)
            cash.delete()

    #Else will work this code
    App_Id = "cd4ae38185273442f9a802c3b3a02665"
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                       params={'lat': lat, 'lon' : lon, 'cnt': '16', 'units': 'metric', 'lang': 'ru', 'APPID': App_Id})
    data = res.json()
    data_list = []

    advices = []

    for a in data['list']:
        temp = a['main']['temp']
        humidity = a['main']['humidity']
        wind = a['wind']['speed']
        weather_id = a['weather'][0]['id']
        # Create advice list
        advices = []
        if temp >= 50:
            advices.append('Ужасная жара, выходить на улицу опасно!')
        elif temp >= 40:
            advices.append('Очень жарко, опасайтесь солнечного удара')
        elif temp >= 30:
            advices.append('Жарко, одевайтесь легче')
        elif temp >= 20:
            advices.append('Тепло, можно надеть футболку и шорты')
        elif temp >= 10:
            advices.append('Прохладно, не одевайтесь слишком легко')
        elif temp >= 2:
            advices.append('Холодно, одевайтесь теплее, не забудьте шапку')
        elif (-2 <= temp) and (temp < 2):
            advices.append('Возможен мокрый снег и гололёд')
        elif temp >= -10:
            advices.append('Температура уже ниже нуля, одевайтесь теплее')
        elif temp <= -20:
            advices.append("Мороз! Обязательно одевайте пуховики, теплые шапки и перчатки")
        elif temp >= -30:
            advices.append('Сильный мороз, одевайте пуховики, шапки ушанки, валенки, а лучше не выходите из дома!')
        elif temp < -30:
            advices.append('Ужасно холодно, выходить на улицу опасно для жизни!')

        if wind >= 32:
            advices.append('На улице ураган! Ни в коем случае не выходите наружу!')
        elif wind >= 20:
            advices.append('На улице шторм! Не выходите из дома!')
        elif wind >= 17:
            advices.append('Сильный ветер. Будте осторожны')
        elif wind >= 10:
            advices.append('Ветренно, не забудьте ветровку')
        elif wind >= 5:
            advices.append('На улице умеренный ветер, можно запускать воздуного змея')
        elif wind >= 3:
            advices.append('Слабый ветер, хорошая погода для прогулки')
        elif wind >= 1:
            advices.append('Ветра почти нет, вас не продует')
        elif wind >= 0:
            advices.append('Ветра нету, можно выйти погулять')

        if (humidity >= 0) and (humidity <= 10):
            advices.append('Очень низкая влажность, не рекомендуем проветривание помещений')
        elif temp < -5:
            advices.append('Низкая влажность, не рекомендуем проветривание помещений')
        elif (humidity > 10 and humidity < 40):
            advices.append('Влажность ниже комфортной, возможно потребуется увлажнитель воздуха')
        elif (humidity >= 40 and humidity <= 60):
            advices.append('На улице комфортная влажность, самое время для прогулки')
        elif (humidity > 60 and humidity < 90):
            advices.append('Влажность выше комфортной, возможно потребуется осушитель воздуха')
        elif (humidity >= 90 and humidity <= 100):
            advices.append('Очень высокая влажность, лучше не проветривать дом')
        # Specifics cases                                                                                    #-56
        if (weather_id >= 200 and weather_id <= 299):
            advices.append('На улице гроза, не берите с собой никаких железных предметов')

        if (weather_id >= 300 and weather_id <= 399):
            advices.append('Моросит лёгкий дождь, не забудьте зонт')

        if (weather_id >= 500 and weather_id <= 531):
            advices.append('Дождь, лучше одеть непромакаемую обувь и взять зонт')

        if weather_id >= 600 and weather_id <= 699:
            advices.append('Снегопад, стоит одеть зимнюю обувь')

        if weather_id == 800 and (temp >= 15 and temp <= 25):
            advices.append('Сегодня отличная погода для прогулки!')

        if (weather_id >= 700 and weather_id <= 721) or (weather_id == 741):
            advices.append('Плохая видимость, туман. Воздержитесь от поездок на машине')

        if (weather_id >= 761 and weather_id <= 762) or (weather_id == 731):
            advices.append('Пылевые бури! Подготовте защиту для глаз!')

        if (weather_id >= 771 and weather_id <= 781) or (weather_id >= 957 and weather_id <= 962) or (
                weather_id >= 900 and weather_id <= 902):
            advices.append('Шквалистый ветер! Не выходите на улицу без необходимости!')

        if (weather_id >= 611 and weather_id <= 616):
            advices.append('Слякоть и мокрый снег, лучше не одевать новую одежду и обувь')

        if (humidity >= 40 and humidity <= 60) and (temp >= 15 and temp <= 30):
            advices.append('На улице идеальная влажность, самое время проветрить квартиру')

        if (humidity >= 60 and humidity <= 100) and (temp <= 15) and (wind >= 10):
            advices.append('Холдный влажный ветер, рекомендуем одеть шарф')

        if (humidity >= 0 and humidity <= 40) and (temp >= 30):
            advices.append('Жаркая сухая погода, обязательно возмите воду с собой')

        if (weather_id >= 600 and weather_id <= 699) and (humidity >= 60 and humidity <= 100):
            advices.append('Опасно, возможны обрывы проводов!')
            # End advice list

        day_weather = {'temp': temp, 'humidity':humidity, 'wind': wind,
                       'weather_id' : weather_id, 'img' : a['weather'][0]['icon'], 'advices' : advices}

        data_list.append(day_weather)

    delta_date = (datetime.date(datetime(int(year), int(month), int(day))) - datetime.now().date()).days
    requested_temp = data_list[delta_date]['temp']
    requested_humidity = data_list[delta_date]['humidity']
    requested_wind = data_list[delta_date]['wind']
    weather_id = data_list[delta_date]['weather_id']

    path_m = 'results/res-man' + '_' + year + '_' + month + '_' + day + '-' + lat + '-' + lon + '.png'
    path_f = 'results/res-woman' + '_' + year + '_' + month + '_' + day + '-' + lat + '-' + lon + '.png'
    Scotcher(True, requested_temp, requested_humidity, requested_wind, weather_id).save(os.getcwd() + '/MainApp/static/' + path_m)
    Scotcher(False, requested_temp, requested_humidity, requested_wind, weather_id).save(os.getcwd() + '/MainApp/static/' + path_f)
    json_dict = {'url': {'man': 'static/results/res-man' + '_' + year + '_' + month + '_' + day + '-' + lat + '-' + lon + '.png',
                         'woman': 'static/results/res-woman' + '_' + year + '_' + month + '_' + day + '-' + lat + '-' + lon + '.png'},
                 'data': data_list}
    models.request.objects.create(date=year + '-' + month + '-' + day,
                                  lat=lat, lon=lon, json=json.dumps(json_dict), res_file_name_m=path_m, res_file_name_f=path_f)

    if method == "html":
        context = {
            'res_path_m': path_m,
            'res_path_f': path_f,
            'advices' : advices,
        }
        return render(request, "index.html", context)
    response = JsonResponse(json_dict)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def Scotcher(man, temp, humidity, wind, weather_id):

    Garb = models.garb.objects
    path = os.getcwd() + "/MainApp/static/source/"

    if not man:
        bg = Image.open(path + Garb.get(ident=0).file_name)
        body = Image.open(path + Garb.get(ident=199).file_name)

        hat = None
        scarf = None
        shirt = None
        vest = None
        pants = None
        boots = None

        # Different temp
        if temp > 30:
            shirt = Image.open(path + Garb.get(ident=110).file_name) #Футболка
            pants = Image.open(path + Garb.get(ident=130).file_name) #Шорты
            boots = Image.open(path + Garb.get(ident=141).file_name) #Сандали!

        elif temp > 20:
            shirt = Image.open(path + Garb.get(ident=110).file_name)
            pants = Image.open(path + Garb.get(ident=131).file_name)
            boots = Image.open(path + Garb.get(ident=141).file_name)
            if wind > 12:
                shirt = Image.open(path + Garb.get(ident=120).file_name) #Ветровка!

        elif temp > 10:
            shirt = Image.open(path + Garb.get(ident=112).file_name) #Толстовка!
            vest = Image.open(path + Garb.get(ident=121).file_name)
            pants = Image.open(path + Garb.get(ident=131).file_name)
            boots = Image.open(path + Garb.get(ident=141).file_name)

        elif temp > 0:
            hat = Image.open(path + Garb.get(ident=102).file_name)
            shirt = Image.open(path + Garb.get(ident=112).file_name)
            vest = Image.open(path + Garb.get(ident=121).file_name)
            pants = Image.open(path + Garb.get(ident=131).file_name)
            boots = Image.open(path + Garb.get(ident=141).file_name)

        elif temp > -9:
            hat = Image.open(path + Garb.get(ident=102).file_name)
            scarf = Image.open(path + Garb.get(ident=160).file_name)
            shirt = Image.open(path + Garb.get(ident=112).file_name)
            vest = Image.open(path + Garb.get(ident=122).file_name)
            pants = Image.open(path + Garb.get(ident=132).file_name)
            boots = Image.open(path + Garb.get(ident=142).file_name)

        elif temp < -8:
            hat = Image.open(path + Garb.get(ident=103).file_name)
            scarf = Image.open(path + Garb.get(ident=160).file_name)
            shirt = Image.open(path + Garb.get(ident=112).file_name)
            vest = Image.open(path + Garb.get(ident=122).file_name)
            pants = Image.open(path + Garb.get(ident=132).file_name)
            boots = Image.open(path + Garb.get(ident=142).file_name)

        # Specifical cases
        if (weather_id >= 200 and weather_id <= 399) or (weather_id >= 500 and weather_id <= 531):
            umbrella = Image.open(path + Garb.get(ident=50).file_name)
            boots = Image.open(path + Garb.get(ident=43).file_name)
            body.paste(umbrella, (Garb.get(ident=50).cord_x, Garb.get(ident=50).cord_y), umbrella)

        if weather_id >= 600 and weather_id <= 699:
            boots = Image.open(path + Garb.get(ident=142).file_name)

        if weather_id == 800 and temp > 17:
            hat = None  # Image.open(path + Garb.get(ident=1).file_name) #Кепка!

        hair = Image.open(path + Garb.get(ident=100).file_name)
        body.paste(hair, (0, 0), hair)
        
        if not hat == None:
            body.paste(hat, (0, 0), hat)
        if not shirt == None:
            body.paste(shirt, (0, 0), shirt)
        if not pants == None:
            body.paste(pants, (0, 0), pants)
        if not scarf == None:
            body.paste(scarf, (0, 0), scarf)
        if not vest == None:
            body.paste(vest, (0, 0), vest)


        bg.paste(body, (0, 0), body)

        if not boots == None:
            bg.paste(boots, (70, 0), boots)

        return bg
    else:
        #Getting body of a man
        bg = Image.open(path + Garb.get(ident=0).file_name)
        body = Image.open(path + Garb.get(ident=99).file_name)

        hat = None
        scarf = None
        shirt = None
        vest = None
        pants = None
        boots = None

        #Different temp
        if temp > 30:
            shirt = Image.open(path +  Garb.get(ident=10).file_name)
            pants = Image.open(path +  Garb.get(ident=30).file_name)
            boots = Image.open(path +  Garb.get(ident=44).file_name)

        elif temp > 20:
            shirt = Image.open(path +  Garb.get(ident=10).file_name)
            pants = Image.open(path +  Garb.get(ident=31).file_name)
            boots = Image.open(path +  Garb.get(ident=41).file_name)
            if wind > 12:
                vest = Image.open(path +  Garb.get(ident=20).file_name)

        elif temp > 10:
            shirt = Image.open(path +  Garb.get(ident=11).file_name)
            vest = Image.open(path +  Garb.get(ident=21).file_name)
            pants = Image.open(path +  Garb.get(ident=31).file_name)
            boots = Image.open(path +  Garb.get(ident=41).file_name)

        elif temp > 0:
            hat = Image.open(path + Garb.get(ident=2).file_name)
            shirt = Image.open(path +  Garb.get(ident=12).file_name)
            vest = Image.open(path +  Garb.get(ident=21).file_name)
            pants = Image.open(path +  Garb.get(ident=31).file_name)
            boots = Image.open(path +  Garb.get(ident=41).file_name)

        elif temp > -9:
            hat = Image.open(path +  Garb.get(ident=2).file_name)
            scarf = Image.open(path +  Garb.get(ident=60).file_name)
            shirt = Image.open(path +  Garb.get(ident=11).file_name)
            vest = Image.open(path +  Garb.get(ident=22).file_name)
            pants = Image.open(path +  Garb.get(ident=32).file_name)
            boots = Image.open(path +  Garb.get(ident=42).file_name)

        elif temp < -8:
            hat = Image.open(path +  Garb.get(ident=3).file_name)
            scarf = Image.open(path +  Garb.get(ident=60).file_name)
            shirt = Image.open(path +  Garb.get(ident=12).file_name)
            vest = Image.open(path +  Garb.get(ident=22).file_name)
            pants = Image.open(path +  Garb.get(ident=32).file_name)
            boots = Image.open(path +  Garb.get(ident=42).file_name)

        # Specifical cases
        if (weather_id >= 200 and weather_id <= 399) or (weather_id >= 500 and weather_id <= 531):
            umbrella = Image.open(path + Garb.get(ident=50).file_name)
            boots = Image.open(path + Garb.get(ident=43).file_name)
            body.paste(umbrella, (Garb.get(ident=50).cord_x, Garb.get(ident=50).cord_y), umbrella)

        if weather_id >= 600 and weather_id <= 699:
           boots = Image.open(path + Garb.get(ident=42).file_name)

        if weather_id == 800 and temp > 17:
            hat = None #Image.open(path + Garb.get(ident=1).file_name)

        if not hat == None:
            body.paste(hat, (0, 0), hat)
        if not shirt == None:
            body.paste(shirt, (0, 0), shirt)
        if not pants == None:
            body.paste(pants, (0, 0), pants)
        if not scarf == None:
            body.paste(scarf, (0, 0), scarf)
        if not vest == None:
            body.paste(vest, (0, 0), vest)

        bg.paste(body, (0, 0), body)

        if not boots == None:
            bg.paste(boots, (70, 0), boots)

        return bg

