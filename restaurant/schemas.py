#pydantic схемы для апи
from typing import List
from ninja import Schema


class RestaurantIn(Schema):
    name: str
    address: str

class RestaurantOut(Schema):
    id: int
    name: str
    address: str


class ChefIn(Schema):
    name: str
    restaurant: int

class ChefOut(Schema):
    id: int
    name: str
    restaurant:int


class IngredientIn(Schema):
    name: str

class IngredientOut(Schema):
    id: int
    name: str


class PizzaIn(Schema):
    name: str
    cheese_type: str
    dough_thickness: str
    secret_ingredient: str
    restaurant: int
    ingredients: List[int]

class PizzaOut(Schema):
    id: int
    name: str
    cheese_type: str
    dough_thickness: str
    secret_ingredient: str
    restaurant: int
    ingredients: List[str]


class ReviewIn(Schema):
    restaurant: int
    rating: int
    text: str

class ReviewOut(Schema):
    id: int
    restaurant: int
    rating: int
    text: str