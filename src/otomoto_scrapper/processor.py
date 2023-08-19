from typing import List
import json
import csv

import statistics

from .models import Car


class CarDataProcessor:
    def __init__(self):
        self.cars = []

    def add_cars(self, cars: List[Car]):
        self.cars.extend(cars)

    def write_to_csv(self, filename: str):
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = Car.__annotations__.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for car in self.cars:
                writer.writerow(car.__dict__)

    def write_to_json(self, filename: str):
        car_list = [car.__dict__ for car in self.cars]
        with open(filename, "w", encoding="utf-8") as jsonfile:
            json.dump(car_list, jsonfile, indent=4)

    def read_from_csv(self, filename: str):
        self.cars = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                car = Car(**row)
                self.add_car(car)

    def read_from_json(self, filename: str):
        self.cars = []
        with open(filename, "r", encoding="utf-8") as jsonfile:
            car_list = json.load(jsonfile)
            for car_data in car_list:
                car = Car(**car_data)
                self.add_car(car)

    def print_statistics(self):
        prices = [car.price for car in self.cars]
        mileage = [car.mileage for car in self.cars]
        self.print_cars()
        print("\nStatistics:")
        print(f"Cars Quantity: {len(self.cars)}")
        print("\nPrice Statistics:")
        print(f"Min Price: {min(self.cars, key= lambda x: x.price)} PLN")
        print(f"Median Price: {statistics.median(prices)} PLN")
        print(f"Average Price: {statistics.mean(prices)} PLN")
        print("\nMileage Statistics:")
        print(f"Min Mileage: {min(self.cars, key= lambda x: x.mileage)} km")
        print(f"Median Mileage: {statistics.median(mileage)} km")
        print(f"Average Mileage: {statistics.mean(mileage)} km")

    def print_cars(self):
        for c in self.cars:
            print(c)
