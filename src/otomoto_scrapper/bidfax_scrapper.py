from bs4 import BeautifulSoup
from models import SearchFilter, Car
from scrapper import WebScrapper
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class BidfaxWebscrapper(WebScrapper):
    def __init__(self, sf: SearchFilter) -> None:
        self.link = f"https://en.bidfax.info/{sf.brand}/{sf.model}/f/from-year={sf.year[0]}/to-year={sf.year[1]}/"
        self.search_filter = sf
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def get_page(self, page: int, wait_time=2):
        link = self.link + f"/page/{page}/"
        self.driver.get(link)
        self.driver.implicitly_wait(wait_time)
        page_content = self.driver.page_source
        soup = BeautifulSoup(page_content, "html.parser")
        return soup

    def extract_cars_from(self, soup):
        cars = []
        offers = soup.find("section", class_="new-offers")
        for offer in offers.find_all("div", class_="thumbnail offer"):
            try:
                price = offer.find("span", class_="prices").text
                caption = offer.find("div", class_="caption")
                link = caption.find("a", href=True).get("href")
                name = caption.find("a", href=True).find("h2").text
                for p in caption.find_all("p"):
                    key = p.text.lower()
                    val = p.find("span").text
                    if "mileage" in key:
                        mileage = val.split("\xa0")[0]
                    elif "damage" in key:
                        damage = val
                    elif "condition" in key:
                        condition = val

                c = Car(
                    name=name,
                    mileage=round(int(mileage) * 1.601),
                    year=0,
                    price=round(int(price) * 4.1),
                    link=link,
                    damaged=damage,
                    condition=condition,
                    year=self.search_filter.year[0],
                )
                cars.append(c)
                print("expected price: ", round(c.price * 47000 / (6000 * 4.1)), " PLN")
            except Exception as e:
                print(">>>> exception in ", str(e))

    def close(self):
        self.driver.quit()
