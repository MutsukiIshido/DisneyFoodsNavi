from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    user_permissions = None
    username = None
    
    nickname = models.CharField(max_length=64)
    email = models.EmailField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    USERNAME_FIELD = "nickname"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]
    
    
    class Meta:
        db_table = "users"
        

class Foods(models.Model):
    foods_name = models.CharField(max_length=64)
    price = models.IntegerField()
    foods_image_path = models.CharField(max_length=255)
    total_reviews = models.IntegerField()
    average_rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "foods"
        
    def  __str__(self):
        return self.foods_name


class Areas(models.Model):
    area_name = models.CharField(max_length=64)
    park = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "areas"
        

class Stores(models.Model):
    store_name = models.CharField(max_length=24)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        help_text="Latitude: a value between -90.0 and 90.0"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        help_text="Longitude: a value between -180.0 and 180.0"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    area = models.OneToOneField(Areas, on_delete=models.CASCADE,  related_name="store", default=1)
    foods = models.ManyToManyField(Foods, related_name="foods")
    
    class Meta:
        db_table = "stores"


class FoodStores(models.Model):
    foods = models.ForeignKey(Foods, on_delete=models.CASCADE)
    stores = models.ForeignKey(Stores, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "food_stores"
    
    
class FoodCategories(models.Model):
    foods = models.ForeignKey(Foods, on_delete=models.PROTECT)
    kind = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "food_categories"
        
