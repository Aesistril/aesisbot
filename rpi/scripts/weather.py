from sys import argv
import requests
import asistlib as al
from bs4 import BeautifulSoup

args = al.asistArgs()
city = "istanbul"

args['date'] = args['date'].replace(' ', '+')

def getWeather(date='', ):
    global city

    # creating url and requests instance
    url = "https://www.google.com/search?q="+"weather+"+city+'+'+date
    html = requests.get(url).content
    
    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    
    # formatting data
    data = str.split('\n')
    time = data[0]
    sky = data[1]

    return {'temp':temp, "time":time, "sky":sky}

args['date'] = args['date'].replace('+', ' ')

try:
    weather = getWeather(args['date'])
    al.talk(args['date'] +city+' da hava '+weather['temp']+' '+weather['sky'])
except Exception as err:
    print(err)
    weather = getWeather()
    al.talk('bugün ' +city+' da hava '+weather['temp']+' '+weather['sky'])

