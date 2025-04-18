from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not nickname:
            raise ValueError('The Nickname field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, nickname, password, **extra_fields)



class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    user_permissions = None
    username = None
    
    nickname = models.CharField(max_length=64,unique=True) # Uniqueを追加
    email = models.EmailField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    USERNAME_FIELD = "nickname"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]
    
    objects = CustomUserManager()  # カスタムマネージャーを指定

    
    class Meta:
        db_table = "users"


class FoodCategory(models.Model):    
    kind = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    class Meta:
        db_table = "food_categories"

        
class Food(models.Model):
    foods_name = models.CharField(max_length=64)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    price = models.IntegerField()
    foods_image_path = models.CharField(max_length=255)
    total_reviews = models.IntegerField()
    average_rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "foods"
        
    def  __str__(self):
        return self.foods_name


class Area(models.Model):
    # parkの選択肢
    PARK_CHOICES = [
        (0, 'ランド'),
        (1, 'シー'),        
    ]
    area_name = models.CharField(max_length=64)
    park = models.IntegerField(choices=PARK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "areas"
        

class Store(models.Model):
    store_name = models.CharField(max_length=24)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="stores")
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stores"

    def __str__(self):
        return self.store_name

class FoodStore(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "food_stores"
        unique_together = ('food', 'store')  # 同じフードとストアの組み合わせを重複させない

    def __str__(self):
        return f"{self.food.foods_name} - {self.store.store_name}"            
        
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'food')
        db_table = "favorites"


class Review(models.Model):
    SCORE_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(verbose_name='レビュースコア', choices=SCORE_CHOICES, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        db_table = "reviews"
        
    def get_percent(self):
        percent = round(self.rating / 5 * 100)
        return percent
        
   
    
class ReviewImages(models.Model):
    review_image_path = models.ImageField(upload_to='review_images/', blank=True, null=True) # blank=True, null=Trueとは画像は必須ではないこと示す
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review = models.ForeignKey(Review, related_name='images', on_delete=models.CASCADE)

    class Meta:
        db_table = "review_images"
        