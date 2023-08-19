import time
from src.otomoto_scrapper.processor import CarDataProcessor
from src.otomoto_scrapper.bidfax_scrapper import BidfaxWebScrapper
from src.otomoto_scrapper.models import SearchFilter

from src.otomoto_scrapper.otomoto_scrapper import OtomotoWebScrapper


def scan(sf: SearchFilter, webscrapper, pages_limit=10):
    bws = webscrapper(sf)
    cdp = CarDataProcessor()
    for i in range(1, pages_limit + 1):
        soup = bws.get_page(i)
        cdp.add_cars(bws.extract_cars_from(soup))
    cdp.print_statistics()
    return cdp


def main():
    sf = SearchFilter(brand="audi", model="a4", year=(2015, 2015), broken=False)

    otomoto_dp = scan(sf, OtomotoWebScrapper, 5)
    bidfax_dp = scan(sf, BidfaxWebScrapper, 10)
    bidfax_dp.write_to_csv("bidfax.csv")
    otomoto_dp.write_to_csv("otomoto.csv")


# audi a4 2016 nowa generacja
# audi q5 2016 nowa generacja
# audi q3 2018 nowa generacja
# bmw x3  2017 nowa generacja
# Alfa Romeo Giulia 2015

if __name__ == "__main__":
    main()
