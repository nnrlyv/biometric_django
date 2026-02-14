#endpoints
from ninja import NinjaAPI
from typing import List
from . import schemas, selectors, services
from ninja.errors import HttpError

api = NinjaAPI(title="Алмұрт-ата")


@api.get("/restaurants/", response=List[schemas.RestaurantOut], tags=["Restaurants"])
def list_restaurants(request) -> List[schemas.RestaurantOut]:
    restaurants = selectors.get_restaurants()
    if not restaurants:
        raise HttpError(404, "Restaurants not found")
    return restaurants


@api.post("/restaurants/", response=schemas.RestaurantOut, tags=["Restaurants"])
def create_restaurant(
    request,
    payload: schemas.RestaurantIn
) -> schemas.RestaurantOut:
    return services.create_restaurant(payload)


@api.get("/chefs/", response=List[schemas.ChefOut], tags=["Chefs"])
def list_chefs(request) -> List[schemas.ChefOut]:
    chefs = selectors.get_chefs()
    if not chefs:
        raise HttpError(404, "Chefs not found")
    return chefs


@api.post("/chefs/", response=schemas.ChefOut, tags=["Chefs"])
def create_chef(
    request,
    payload: schemas.ChefIn
) -> schemas.ChefOut:
    return services.create_chef(payload)


@api.get("/ingredients/", response=List[schemas.IngredientOut], tags=["Ingredients"])
def list_ingredients(request) -> List[schemas.IngredientOut]:
    ingredients = selectors.get_ingredients()
    if not ingredients:
        raise HttpError(404, "Ingredients not found")
    return ingredients


@api.post("/ingredients/", response=schemas.IngredientOut, tags=["Ingredients"])
def create_ingredient(
    request,
    payload: schemas.IngredientIn
) -> schemas.IngredientOut:
    return services.create_ingredient(payload)


@api.get("/pizzas/", response=List[schemas.PizzaOut], tags=["Pizzas"])
def list_pizzas(request) -> List[schemas.PizzaOut]:
    pizzas = selectors.get_pizzas()
    if not pizzas:
        raise HttpError(404, "Pizzas not found")
    return pizzas


@api.post("/pizzas/", response=schemas.PizzaOut, tags=["Pizzas"])
def create_pizza(
    request,
    payload: schemas.PizzaIn
) -> schemas.PizzaOut:
    return services.create_pizza(payload)


@api.put("/pizzas/{pizza_id}/", response=schemas.PizzaOut, tags=["Pizzas"])
def update_pizza(
    request,
    pizza_id: int,
    payload: schemas.PizzaIn
) -> schemas.PizzaOut:
    return services.update_pizza(pizza_id, payload)


@api.delete("/pizzas/{pizza_id}/", tags=["Pizzas"])
def delete_pizza(
    request,
    pizza_id: int
):
    services.delete_pizza(pizza_id)
    return {"success": "Your pizza was deleted"}


@api.get("/reviews/", response=List[schemas.ReviewOut], tags=["Reviews"])
def list_reviews(request) -> List[schemas.ReviewOut]:
    reviews = selectors.get_reviews()
    if not reviews:
        raise HttpError(404, "Reviews not found")
    return reviews



@api.post("/reviews/", response=schemas.ReviewOut, tags=["Reviews"])
def create_review(
    request,
    payload: schemas.ReviewIn
) -> schemas.ReviewOut:
    return services.create_review(payload)



@api.get("/restaurants/{restaurant_id}/menu/", tags=["Menu"])
def restaurant_menu(
    request,
    restaurant_id: int
):
    restaurant, pizzas = selectors.get_restaurant_menu(restaurant_id)
    if not restaurant:
        raise HttpError(404, "Restaurant not found")
    return {
        "restaurant": restaurant.name,
        "menu": pizzas
    }
