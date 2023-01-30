from helium import *
from bs4 import BeautifulSoup
from mileagefunction import mileage_grepper
import csv



## Checking price if article is a car or not. Car == price over 20 000 kr
def isCar(x):
    try:
        pricetest = x.text
    except AttributeError:
        return
    pricetest = pricetest[:-3]
    pricetest = pricetest.replace(" ", "")
    try:
        return int(pricetest)
    except ValueError:
        return



## Generating request link depending on amount of pages wanted 
def PageScan(x :int):
    x = int(x)
    if x == 1:
        return "https://www.blocket.se/annonser/hela_sverige?q=Tesla&st=s"
    else:
        return f"https://www.blocket.se/annonser/hela_sverige?page={x}&q=Tesla&st=s"



## Article Class for storing title, price and location in list.
class TeslaArticle:

    products = []

    def __init__(self, title, price, location, year, mileage):
        self.title = title
        self.price = price
        self.location = location
        self.year = year
        self.mileage = mileage
        self.add_to_products()

    def add_to_products(self):
        TeslaArticle.products.append(self)



# Main function, fetching different elements before storing in TeslaArticle Class
def fetcher():

    for quote in quotes:

        # Price of article
        price = quote.find('div', {'class': 'hAKWLn'})

        # Checking price, if lower than 20 000, skipping current itteration
        try:
            if isCar(price) < 20000:
                continue
        except TypeError:
            continue

        # Title of article
        title = quote.find('span', {'class': 'dvfBcm'})
        # Location of article
        location = quote.find('a', {'class': 'kpERIC'})
        # Year of article
        year = quote.find('li', {'class': 'eVpFlC'})
        # Mileage of article
        mileage = mileage_grepper(quote)


        if location == None:
            location = "Location not found"
            TeslaArticle(title.text, price.text, location, year.text, mileage)
        else:
            TeslaArticle(title.text, price.text, location.text, year.text, mileage)


    
# Asking user amount of pages to scrape
amount_pages = input("How many pages to scrape?: ")

# Converting to int
amount_pages = int(amount_pages)

#Making sure one initial scrape is done, because the links change depending on if it's page 1 or above.

# Starts headless page
browser = start_chrome(PageScan(1), headless=True)

# Putting source code through parser
soup = BeautifulSoup(browser.page_source, "html.parser")

# Finds all articles
quotes = soup.find_all('article', {'class': 'eMSBWP'})

# Main function
fetcher()



# Making additional scrapes if times run shall be above 1
if amount_pages >= 2:
    for i in range(amount_pages):
        browser = start_chrome(PageScan(i), headless=True)

        soup = BeautifulSoup(browser.page_source, "html.parser")

        quotes = soup.find_all('article', {'class': 'eMSBWP'})

        fetcher()


# I have no clue of what I'm doing here.


# Printing for debugging
for product in TeslaArticle.products:
    print(product.title, "\n", "Price:", product.price, "\n", "Location:", product.location, "\n", "Model Year:", product.year, "\n", "Mileage:", product.mileage)


# Preparing items in lists so I can write to CSV.
cartitles = []
carprices = []
carlocations = []
caryears = []
carmileages = []
for product in TeslaArticle.products:
    cartitles.append(product.title)
for product in TeslaArticle.products:
    carprices.append(product.price)
for product in TeslaArticle.products:
    carlocations.append(product.location)
for product in TeslaArticle.products:
    caryears.append(product.year)
for product in TeslaArticle.products:
    carmileages.append(product.mileage)


# More Debugging and writing to CSV.
print(cartitles)
f = open("articles.csv", "a", newline="")
writer = csv.writer(f)
writer.writerow(cartitles)
writer.writerow(carprices)
writer.writerow(carlocations)
writer.writerow(caryears)
writer.writerow(carmileages)


# End browser process
kill_browser()