#бизнес логика
from django.shortcuts import get_object_or_404
from .models import Restaurant, Chef, Pizza, Ingredient, Review


def create_restaurant(data):
    return Restaurant.objects.create(name=data.name, address=data.address)


def create_chef(data):
    restaurant = get_object_or_404(Restaurant, id=data.restaurant)

    if hasattr(restaurant, "chef"):
        raise ValueError("This restaurant already has a chef.")

    return Chef.objects.create(name=data.name, restaurant=restaurant)


def create_ingredient(data):
    return Ingredient.objects.create(name=data.name)


def create_pizza(data):
    restaurant = get_object_or_404(Restaurant, id=data.restaurant)

    pizza = Pizza.objects.create(
        name=data.name,
        cheese_type=data.cheese_type,
        dough_thickness=data.dough_thickness,
        secret_ingredient=data.secret_ingredient,
        restaurant=restaurant,
    )

    pizza.ingredients.set(data.ingredients)
    return pizza


def update_pizza(pizza_id, data):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    restaurant = get_object_or_404(Restaurant, id=data.restaurant)

    pizza.name = data.name
    pizza.cheese_type = data.cheese_type
    pizza.dough_thickness = data.dough_thickness
    pizza.secret_ingredient = data.secret_ingredient
    pizza.restaurant = restaurant
    pizza.save()
    pizza.ingredients.set(data.ingredients)

    return pizza


def delete_pizza(pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    pizza.delete()


def create_review(data):
    if data.rating > 5:
        raise ValueError("Rating cannot be more than 5")

    restaurant = get_object_or_404(Restaurant, id=data.restaurant)

    return Review.objects.create(
        restaurant=restaurant,
        rating=data.rating,
        text=data.text,
    )
