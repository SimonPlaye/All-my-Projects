import os
import csv
import requests
from bs4 import BeautifulSoup

requete = requests.get("https://www.facebook.com/AmbreRiv/about")
page = requete.content
soup = BeautifulSoup(page, features="html.parser")
a=soup.find('u1',{'class':'uiList _54nz _4kg _4kt'})
print(a)