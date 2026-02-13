from django.http import HttpResponse
from ninja import NinjaAPI, Schema
from typing import List
from .models import Restaurant, Chef, Pizza, Ingredient, Review
from django.shortcuts import get_object_or_404
from ninja.errors import Http404
api = NinjaAPI(title="Алмұрт-ата")


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


@api.get("/restaurants/", response=List[RestaurantOut], tags=["Restaurants"])
def list_restaurants(request):
    return Restaurant.objects.all()

@api.post("/restaurants/", tags=["Restaurants"])
def create_restaurant(request, payload: RestaurantIn):
    restaurant = Restaurant.objects.create(name=payload.name, address=payload.address)
    return RestaurantOut(id=restaurant.id, name=restaurant.name, address=restaurant.address)


@api.get("/chefs/", response=List[ChefOut], tags=["Chefs"])
def list_chefs(request):
    chefs = Chef.objects.all()
    return [
            {
                "id": chef.id,
                "name": chef.name,
                "restaurant": chef.restaurant_id
            }
            for chef in chefs
        ]

@api.post("/chefs/",tags=["Chefs"])
def create_chef(request, payload: ChefIn):
    restaurant_obj = get_object_or_404(Restaurant, id=payload.restaurant)
    if hasattr(restaurant_obj, "chef"):
        return {"error": "This restaurant already has a chef."}
    chef = Chef.objects.create(name=payload.name, restaurant=restaurant_obj)
    return ChefOut(id=chef.id, name=chef.name, restaurant=chef.restaurant_id)



@api.post("/ingredients/", response=IngredientIn, tags=["Ingredients"])
def create_ingredient(request, payload: IngredientIn):
    i = Ingredient.objects.create(name=payload.name)
    return IngredientOut(id=i.id, name=i.name)


@api.get("/ingredients/", response= List[IngredientOut], tags=["Ingredients"])
def list_ingredients(request):
    ingredients = Ingredient.objects.all()
    return ingredients


@api.get("/pizzas/", response=List[PizzaOut], tags=["Pizzas"])
def list_pizzas(request):
    pizzas = Pizza.objects.all()
    result = []
    for p in pizzas:
        result.append(PizzaOut(
            id= p.id,
            name=p.name,
            cheese_type=p.cheese_type,
            dough_thickness=p.dough_thickness,
            secret_ingredient=p.secret_ingredient,
            restaurant=p.restaurant.id,
            ingredients= [i.name for i in p.ingredients.all()]
        ))
    return result



@api.post("/pizzas/", tags=["Pizzas"])
def create_pizza(request, payload: PizzaIn):
    restaurant_obj = get_object_or_404(Restaurant, id=payload.restaurant)
    pizza = Pizza.objects.create(
        name=payload.name,
        cheese_type=payload.cheese_type,
        dough_thickness=payload.dough_thickness,
        secret_ingredient=payload.secret_ingredient,
        restaurant=restaurant_obj
    )

    pizza.ingredients.set(payload.ingredients)

    return PizzaOut(
        id=pizza.id,
        name=pizza.name,
        cheese_type=pizza.cheese_type,
        dough_thickness=pizza.dough_thickness,
        secret_ingredient=pizza.secret_ingredient,
        restaurant=pizza.restaurant.id,
        ingredients= [i.name for i in pizza.ingredients.all()]

    )

@api.put("/pizzas/{pizza_id}/", response=PizzaIn, tags=["Pizzas"])
def update_pizza(request, pizza_id: int, payload: PizzaIn):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    restaurant_obj = get_object_or_404(Restaurant, id=payload.restaurant)
    pizza.name = payload.name
    pizza.cheese_type = payload.cheese_type
    pizza.dough_thickness = payload.dough_thickness
    pizza.secret_ingredient = payload.secret_ingredient
    pizza.restaurant = restaurant_obj
    pizza.save()
    pizza.ingredients.set(payload.ingredients)
    return payload

@api.delete("/pizzas/{pizza_id}/", tags=["Pizzas"])
def delete_pizza(request, pizza_id: int):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    pizza.delete()
    return {"success": "Your pizza was deleted"}


@api.get("/reviews/", response=List[ReviewOut], tags=["Reviews"])
def list_reviews(request):
    reviews = Review.objects.all()
    return [ReviewOut(
        id=r.id,
        restaurant=r.restaurant.id,
        rating=r.rating,
        text=r.text
    ) for r in reviews]

@api.post("/reviews/",tags=["Reviews"])
def create_review(request, payload: ReviewIn):
    if payload.rating > 5:
        return  HttpResponse("Rating cannot be more than 5", status = 404)

    restaurant_obj = get_object_or_404(Restaurant, id=payload.restaurant)
    r = Review.objects.create(
        restaurant=restaurant_obj,
        rating=payload.rating,
        text=payload.text
    )


    return ReviewIn(
        restaurant=r.restaurant.id,
        rating=r.rating,
        text=r.text
    )


@api.get("/restaurants/{restaurant_id}/menu/", tags=["Menu"])
def restaurant_menu(request, restaurant_id: int):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return {"msg": "Restaurant not found"}

    pizzas = []
    for p in restaurant.pizzas.all():
        pizzas.append(PizzaOut(
            id=p.id,
            name=p.name,
            cheese_type=p.cheese_type,
            dough_thickness=p.dough_thickness,
            secret_ingredient=p.secret_ingredient,
            restaurant=p.restaurant.id,
            ingredients = [ing.name for ing in p.ingredients.all()]

        ))
    return {"restaurant": restaurant.name, "menu": pizzas}
