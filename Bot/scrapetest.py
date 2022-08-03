from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs4


def getHtml(url):
    try:
        html=urlopen(url)
    except:
        print("error")
        return None

    try:
        soup=bs4(html.read(), features='lxml')
    except:
        print("error")
        return None

    rt_list=soup.find_all("",{"href":"/home"})
    print(soup)

getHtml("https://twitter.com/realDonaldTrump")
