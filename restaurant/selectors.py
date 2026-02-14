from django.shortcuts import get_object_or_404
from .models import Restaurant, Chef, Pizza, Ingredient, Review


def get_restaurants():
    return Restaurant.objects.all()


def get_chefs():
    return Chef.objects.all()


def get_ingredients():
    return Ingredient.objects.all()


def get_pizzas():
    return Pizza.objects.prefetch_related("ingredients", "restaurant")


def get_reviews():
    return Review.objects.select_related("restaurant")


def get_restaurant_menu(restaurant_id: int):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    pizzas = restaurant.pizzas.prefetch_related("ingredients")
    return restaurant, pizzas
