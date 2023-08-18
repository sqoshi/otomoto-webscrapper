from models import SearchFilter, Car
from scrapper import WebScrapper


class BidfaxWebscrapper(WebScrapper):
    def __init__(self, sf: SearchFilter) -> None:
        # self.link = f"https://en.bidfax.info/{sf.brand}/{sf.model}/f/from-year={sf.year[0]}/to-year={sf.year[1]}"
        self.link = f"https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&year-from={sf.year[0]}&year-to={sf.year[1]}&make={sf.brand.replace(' ','%20')}&model={sf.model}&auction-type=All"

    def get_page(self, page: int):
        link = self.link + f"&page={page}"

        print(link)
        return self.get_soup(link)

    def extract_cars_from(self, soup):
        offers = soup.find("main", class_="main")
        print(offers)
        offers = soup.find("main", class_="new-offers")
        # offers = soup.find('section', class_="content  clearfix")
        articles = offers.find("div", class_="thumbnail offer")
        for article in articles:
            print(article)


if __name__ == "__main__":
    sf = SearchFilter(brand="bmw", model="x3", year=(2015, 2015), broken=False)
    ws = BidfaxWebscrapper(sf)
    page = ws.get_page(1)
    print(page)
    # ws.extract_cars_from(page)
