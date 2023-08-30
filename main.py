import pandas as pd
from src.otomoto_scrapper.processor import CarDataProcessor
from src.otomoto_scrapper.bidfax_scrapper import BidfaxWebScrapper
from src.otomoto_scrapper.models import SearchFilter
from pytrends.request import TrendReq

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
    # sf = SearchFilter(brand="audi", model="a4", year=(2015, 2015), broken=False)
    sf = SearchFilter(brand="bmw", model="x3", year=(2015, 2015), broken=False)

    otomoto_dp = scan(sf, OtomotoWebScrapper, 5)
    bidfax_dp = scan(sf, BidfaxWebScrapper, 4)
    compare_avg_profit(otomoto_dp, bidfax_dp)
    bidfax_dp.write_to_csv(f"{sf.brand}_{sf.model}_{sf.year[0]}_bidfax.csv")
    otomoto_dp.write_to_csv(f"{sf.brand}_{sf.model}_{sf.year[0]}_otomoto.csv")


def compare_avg_profit(otomoto_dp, bidfax_dp):
    otomoto_avg = sum([x.price for x in otomoto_dp.cars]) / len(otomoto_dp.cars)
    accept_conds = ["Enhanced Vehicles", "Run and Drive"]
    cars = [c for c in bidfax_dp.cars if c.condition in accept_conds]
    bidfax_avg = sum([x.price for x in cars]) / len(cars)
    expected_price = round(bidfax_avg * 47000 / (6000 * 4.1))
    print("Otomoto avg price: ", otomoto_avg, " PLN")
    print(f"Bidfax condition:'{accept_conds}' avg price: ", bidfax_avg, " PLN")
    print("Expected price: ", expected_price, " PLN")
    print("Potential profit: ", otomoto_avg - expected_price, " PLN")


def find_popular_year(search_filters):
    merged_results = []
    for sf in search_filters:
        pytrends = TrendReq(hl="en-US", tz=360)
        for i in range(1, 2 + 1):
            kw_list = [
                f"{sf.brand} {sf.model} {year}"
                for year in range(2010 + (5 * (i - 1)), 2010 + (5 * i))
            ]
            pytrends.build_payload(kw_list, timeframe="today 12-m", geo="PL")
            data = pytrends.interest_over_time()
            column_sums = data.drop(columns="isPartial").sum()
            merged_results.append(column_sums)
    result_df = pd.concat(merged_results)
    sorted_result_df = result_df.sort_values(ascending=False)
    print(sorted_result_df)


def compare_models():
    compared_cars = ("audi q5", "audi q3", "audi a4", "bmw x3", "nissan qashqai")
    filters = [
        SearchFilter(brand=c.split()[0], model=c.split()[-1], year=0, broken=False)
        for c in compared_cars
    ]
    find_popular_year(filters)


# audi a4 2016 nowa generacja
# audi q5 2016 nowa generacja
# audi q3 2018 nowa generacja
# bmw x3  2017 nowa generacja
# Alfa Romeo Giulia 2015

if __name__ == "__main__":
    # main()
    compare_models()
