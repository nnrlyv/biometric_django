# таблицы бд
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Chef(models.Model):
    name = models.CharField(max_length=100)
    restaurant= models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name="chef")

class Ingredient(models.Model):
    name = models.CharField(max_length=50)

class Pizza(models.Model):
    dough_thickness = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    cheese_type = models.CharField(max_length=50)
    secret_ingredient = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="pizzas")
    ingredients = models.ManyToManyField(Ingredient, related_name="pizzas", blank=True)

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    text = models.TextField()
