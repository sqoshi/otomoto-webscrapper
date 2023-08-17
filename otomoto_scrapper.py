from typing import Tuple
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import threading


@dataclass
class Car:
    name: str
    mileage: int  # km
    year: int
    price: int  # pln
    link: str


@dataclass
class SearchFilter:
    brand: str
    model: str
    year: Tuple[int, int]
    broken: bool

class WebScrapper:
    pass

class BidfaxWebscrapper:
        def __init__(self, sf: SearchFilter) -> None:
            self.link = f"https://en.bidfax.info/{sf.brand}/{sf.model}/f/from-year={sf.year[0]}/to-year={sf.year[1]}"
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

        def get_page(self, page: int):
            link = self.link + f"/page/{page}/"
            print(f"Scrapping: {link}\n")
            resp = requests.get(link, self.headers).text
            soup = BeautifulSoup(resp, "html.parser")
            return soup

class OtomotoWebscrapper:
    def __init__(self, sf: SearchFilter) -> None:
        broken_search = "search%5Bfilter_enum_damaged%5D=0&" if not sf.broken else ""
        self.link = f"https://www.otomoto.pl/osobowe/{sf.brand}/{sf.model}/od-{sf.year[0]}?{broken_search}search%5Bfilter_float_year%3Ato%5D={sf.year[1]}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def get_page(self, page: int):
        link = self.link + f"&page={page}"
        print(f"Scrapping: {link}\n")
        resp = requests.get(link, self.headers).text
        soup = BeautifulSoup(resp, "html.parser")
        return soup

    def extract_cars_from(self, soup):
        offers = soup.find("main")
        # for x in soup.find("div", class_="ooa-1u8qly9").find_all("li"):
        #     print(x)
        articles = offers.find_all("article", class_="ooa-1t80gpj ev7e6t818")
        cars = []
        for article in articles:
            try:
                link = article.find("a", href=True).get("href")
                name = article.find("a", href=True).text
                price = article.find("h3").text.replace(" ", "")
                currency = article.find("p", class_="ev7e6t81 ooa-1e3jyoe er34gjf0")
                if currency.text != "PLN":
                    continue
                dds = article.find_all("dd")
                mileage = [
                    el.text.replace(" ", "").replace("km", "")
                    for el in dds
                    if el.get("data-parameter") == "mileage"
                ].pop()
                year = [
                    el.text for el in dds if el.get("data-parameter") == "year"
                ].pop()
                cars.append(Car(name, int(mileage), int(year), int(price), link))
            except Exception as e:
                print(f"exception parsing article: {str(e)}")
        return cars


lock = threading.Lock()


def process_page(page_number, sf, result_list):
    ws = OtomotoWebscrapper(sf)
    soup = ws.get_page(page_number)
    cars = ws.extract_cars_from(soup)
    with lock:
        result_list.extend(cars)


def print_basic_info(all_cars):
    for c in all_cars:
        print(c)
    print()
    print(f"Cars found: {len(all_cars)}")
    print(f"Avg mileage: {sum([c.mileage for c in all_cars])/len(all_cars)} km")
    print(f"Avg price: {sum([c.price for c in all_cars])/len(all_cars)} PLN")
    print(
        f"Median price: {sorted(all_cars, key=lambda x :x.price)[len(all_cars)//2+1]} "
    )
    print(f"Max price model: {max(all_cars, key=lambda x: x.price)} ")
    print(f"Min price model: {min(all_cars, key=lambda x: x.price)} ")
    print(
        f"Min price/(mileage*year): {min(all_cars, key=lambda x: x.price/(x.mileage))} "
    )


if __name__ == "__main__":
    all_cars = []
    threads = []
    max_page = 4
    # sf = SearchFilter(brand="audi", model="q5", year=(2014, 2016), broken=False)
    sf = SearchFilter(brand="bmw", model="x3", year=(2015, 2015), broken=False)
    for i in range(1, max_page + 1):
        thread = threading.Thread(target=process_page, args=(i, sf, all_cars))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if all_cars:
        print_basic_info(all_cars)

# audi a4 2016 nowa generacja
# audi q5 2016 nowa generacja
# audi q3 2018 nowa generacja
# bmw x3  2017 nowa generacja
# Alfa Romeo Giulia 2015