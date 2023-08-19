from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class Car:
    name: str
    mileage: int  # km
    year: int
    price: float  # pln
    link: str
    damaged: Optional[str]
    condition: Optional[str]


@dataclass
class SearchFilter:
    brand: str
    model: str
    year: Tuple[int, int]
    broken: bool
