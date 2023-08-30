from itertools import cycle
from bs4 import BeautifulSoup
from selenium import webdriver

from .models import SearchFilter, Car
from .scrapper import WebScrapper

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

agents = cycle(
    [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    ]
)


class BidfaxWebScrapper(WebScrapper):
    def __init__(self, sf: SearchFilter) -> None:
        self.link = f"https://en.bidfax.info/{sf.brand.lower().replace(' ','-')}/{sf.model}/f/from-year={sf.year[0]}/to-year={sf.year[1]}/"
        self.search_filter = sf
        self.driver = None

    def init_driver(self):
        if self.driver is not None:
            self.driver.quit()

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--headless")
        options.add_argument("--disable-web-security")
        options.add_argument(f"user-agent={next(agents)}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options)

    def get_page(self, page: int, wait_time=1):
        link = self.link + f"page/{page}/"
        print(f"Scrapping {link}")
        self.init_driver()
        self.driver.get(link)
        self.driver.implicitly_wait(wait_time)
        page_content = self.driver.page_source
        soup = BeautifulSoup(page_content, "html.parser")
        print(f"Page: {page}")
        return soup

    def extract_cars_from(self, soup):
        cars = []
        offers = soup.find("section", class_="new-offers")
        for offer in offers.find_all("div", class_="thumbnail offer"):
            if 'script async' in str(offer):
                continue
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
                    price=round(int(price) * 4.1),
                    link=link,
                    damaged=damage,
                    condition=condition,
                    year=self.search_filter.year[0],
                )
                cars.append(c)
                # print("expected price: ", round(c.price * 47000 / (6000 * 4.1)), " PLN")
            except Exception as e:
                print("exception parsing offer: ", str(e))
        print(f"Found cars: {len(cars)}")
        return cars

    def close(self):
        self.driver.quit()
