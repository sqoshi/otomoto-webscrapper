from abc import ABC, abstractmethod
import logging
from typing import List
from bs4 import BeautifulSoup
from models import Car
import requests


class WebScrapper(ABC):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }


    def get_soup(self, link: str) -> BeautifulSoup:
        logging.info(f"Scrapping: {link}\n")
        resp = requests.get(link, self.headers)
        print(
            resp.status_code,
            "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",
        )
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup

    @abstractmethod
    def extract_cars_from(soup: BeautifulSoup) -> List[Car]:
        pass

    # @abstractmethod
    # def extract_max_page(first_page_soup: BeautifulSoup) -> int:
    #     pass
