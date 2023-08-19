import threading
from src.otomoto_scrapper.bidfax_scrapper import BidfaxWebscrapper
from src.otomoto_scrapper.models import SearchFilter

from src.otomoto_scrapper.otomoto_scrapper import OtomotoWebscrapper

lock = threading.Lock()


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


def process_page(page_number, sf, result_list):
    ws = OtomotoWebscrapper(sf)
    soup = ws.get_page(page_number)
    cars = ws.extract_cars_from(soup)
    with lock:
        result_list.extend(cars)


def scan_bidfax(sf: SearchFilter, pages_limit=10):
    bws = BidfaxWebscrapper(sf)
    bidfax_cars = []
    for i in range(1, pages_limit + 1):
        soup = bws.get_page(i)
        bidfax_cars.extend(bws.extract_cars_from(soup))


def main():
    otomoto_cars = []
    threads = []
    max_page = 4
    sf = SearchFilter(brand="bmw", model="x3", year=(2015, 2015), broken=False)
    for i in range(1, max_page + 1):
        thread = threading.Thread(target=process_page, args=(i, sf, otomoto_cars))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if otomoto_cars:
        print_basic_info(otomoto_cars)


# audi a4 2016 nowa generacja
# audi q5 2016 nowa generacja
# audi q3 2018 nowa generacja
# bmw x3  2017 nowa generacja
# Alfa Romeo Giulia 2015

if __name__ == "__main__":
    main()
