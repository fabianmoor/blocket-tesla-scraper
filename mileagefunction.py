from helium import *
from bs4 import BeautifulSoup

url = "https://www.blocket.se/annonser/hela_sverige?q=Tesla&st=s"

browser = start_chrome(url, headless=True)

soup = BeautifulSoup(browser.page_source, "html.parser")

quotes = soup.find_all('div', {'class': 'hQlnrc'})


def mileage_grepper(soup):

    mileage = []

    for div in soup.find_all('div', class_ = "hQlnrc"):
        for ul in div.find_all('ul', class_ = "icmkUf"):
            for li in ul.find_all('li', class_ = "eVpFlC"):
                mileage.append(li.text)        

    newmileage = []
    for i in mileage[2::2]:
        newmileage.append(i)

    mileages = {}
    for i in newmileage[::2]:
        mileages[0] = i

    return mileages[0]
    kill_browser()


