from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class Car:
    name: str
    mileage: int  # km
    year: int
    price: int  # pln
    link: str
    damaged: Optional[str]


@dataclass
class SearchFilter:
    brand: str
    model: str
    year: Tuple[int, int]
    broken: bool
