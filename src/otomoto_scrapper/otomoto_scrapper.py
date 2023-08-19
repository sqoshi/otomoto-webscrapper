from src.otomoto_scrapper.scrapper import WebScrapper
from .models import SearchFilter, Car


class OtomotoWebScrapper(WebScrapper):
    def __init__(self, sf: SearchFilter) -> None:
        broken_search = "search%5Bfilter_enum_damaged%5D=0&" if not sf.broken else ""
        self.link = f"https://www.otomoto.pl/osobowe/{sf.brand}/{sf.model}/od-{sf.year[0]}?{broken_search}search%5Bfilter_float_year%3Ato%5D={sf.year[1]}"

    def get_page(self, page: int):
        link = self.link + f"&page={page}"
        return self.get_soup(link)

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
                cars.append(Car(name, int(mileage), int(year), int(price), link, None, None))
            except Exception as e:
                print(f"exception parsing article: {str(e)}")
        return cars



