import requests
import asistlib as al
from bs4 import BeautifulSoup

word = "kişisel bilgisayar"
word = word.replace(' ', '+')

url = "https://www.google.com/search?q="+word+"+ne+demek"
html = requests.get(url).content

soup = BeautifulSoup(html, 'lxml')
definition = soup.findAll('span', class_='cDrQ7')

print(definition)