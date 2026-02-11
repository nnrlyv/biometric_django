from ninja import NinjaAPI, Schema
from typing import List
from .models import Restaurant, Chef, Pizza, Ingredient, Review
from django.shortcuts import get_object_or_404

api = NinjaAPI(title="Алмұрт-ата")

class RestaurantSchema(Schema):
    id: int = None
    name: str
    address: str

class ChefSchema(Schema):
    id: int = None
    name: str
    restaurant: int

class IngredientSchema(Schema):
    id: int = None
    name: str

class PizzaSchema(Schema):
    id: int = None
    name: str
    cheese_type: str
    dough_thickness: str
    secret_ingredient: str
    restaurant: int
    ingredients: List[int] = []

class ReviewSchema(Schema):
    id: int = None
    restaurant: int
    rating: int
    text: str


@api.get("/restaurants/", response=List[RestaurantSchema], tags=["Restaurants"])
def list_restaurants(request):
    return [RestaurantSchema(id=r.id, name=r.name, address=r.address) for r in Restaurant.objects.all()]

@api.post("/restaurants/", response=RestaurantSchema, tags=["Restaurants"])
def create_restaurant(request, payload: RestaurantSchema):
    r = Restaurant.objects.create(name=payload.name, address=payload.address)
    return RestaurantSchema(id=r.id, name=r.name, address=r.address)

# Menu endpoint
@api.get("/restaurants/{restaurant_id}/menu/", tags=["Menu"])
def restaurant_menu(request, restaurant_id: int):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    pizzas = []
    for p in restaurant.pizzas.all():
        pizzas.append(PizzaSchema(
            id=p.id,
            name=p.name,
            cheese_type=p.cheese_type,
            dough_thickness=p.dough_thickness,
            secret_ingredient=p.secret_ingredient,
            restaurant=p.restaurant.id,
            ingredients=[i.id for i in p.ingredients.all()]
        ))
    return {"restaurant": restaurant.name, "menu": pizzas}


@api.get("/chefs/", response=List[ChefSchema], tags=["Chefs"])
def list_chefs(request):
    return [ChefSchema(id=c.id, name=c.name, restaurant=c.restaurant.id) for c in Chef.objects.all()]

@api.post("/chefs/", response=ChefSchema, tags=["Chefs"])
def create_chef(request, payload: ChefSchema):
    restaurant_obj = get_object_or_404(Restaurant, id=payload.restaurant)
    if hasattr(restaurant_obj, "chef"):
        return {"error": "This restaurant already has a chef."}
    c = Chef.objects.create(name=payload.name, restaurant=restaurant_obj)
    return ChefSchema(id=c.id, name=c.name, restaurant=c.restaurant.id)



@api.post("/ingredients/", response=IngredientSchema, tags=["Ingredients"])
def create_ingredient(request, payload: IngredientSchema):
    i = Ingredient.objects.create(name=payload.name)
    return IngredientSchema(id=i.id, name=i.name)


@api.get("/pizzas/", response=List[PizzaSchema], tags=["Pizzas"])
def list_pizzas(request):
    pizzas = Pizza.objects.all()
    result = []
    for p in pizzas:
        result.append(PizzaSchema(
            id=p.id,
            name=p.name,
            cheese_type=p.cheese_type,
            dough_thickness=p.dough_thickness,
            secret_ingredient=p.secret_ingredient,
            restaurant=p.restaurant.id,
            ingredients=[i.id for i in p.ingredients.all()]
        ))
    return result

@api.post("/pizzas/", response=PizzaSchema, tags=["Pizzas"])
def create_pizza(request, payload: PizzaSchema):
    restaurant_obj = get_object_or_404(Restaurant, id=payload.restaurant)
    p = Pizza.objects.create(
        name=payload.name,
        cheese_type=payload.cheese_type,
        dough_thickness=payload.dough_thickness,
        secret_ingredient=payload.secret_ingredient,
        restaurant=restaurant_obj
    )
    p.ingredients.set(payload.ingredients)
    return PizzaSchema(
        id=p.id,
        name=p.name,
        cheese_type=p.cheese_type,
        dough_thickness=p.dough_thickness,
        secret_ingredient=p.secret_ingredient,
        restaurant=p.restaurant.id,
        ingredients=[i.id for i in p.ingredients.all()]
    )

@api.put("/pizzas/{pizza_id}/", response=PizzaSchema, tags=["Pizzas"])
def update_pizza(request, pizza_id: int, payload: PizzaSchema):
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
    return {"success": True}


@api.get("/reviews/", response=List[ReviewSchema], tags=["Reviews"])
def list_reviews(request):
    reviews = Review.objects.all()
    return [ReviewSchema(
        id=r.id,
        restaurant=r.restaurant.id,
        rating=r.rating,
        text=r.text
    ) for r in reviews]

@api.post("/reviews/", response=ReviewSchema, tags=["Reviews"])
def create_review(request, payload: ReviewSchema):
    restaurant_obj = get_object_or_404(Restaurant, id=payload.restaurant)
    r = Review.objects.create(
        restaurant=restaurant_obj,
        rating=payload.rating,
        text=payload.text
    )
    return ReviewSchema(
        id=r.id,
        restaurant=r.restaurant.id,
        rating=r.rating,
        text=r.text
    )
