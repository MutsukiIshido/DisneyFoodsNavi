from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Food, Review
from django.db.models import Avg, Count
import logging


logger = logging.getLogger(__name__)
print(post_save.has_listeners(Review))

@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_food_rating(sender, instance, **kwargs):
    logger.debug("シグナルが呼び出されました。対象のReview ID: %s", instance.id)
    """
    Reviewの作成、更新、削除時にFoodのaverage_ratingとtotal_reviewsを更新
    """
    food = instance.food
    logger.debug("対象のFood: %s", food.foods_name)
    reviews = Review.objects.filter(food=food)
    
    # 平均評価と口コミ件数を計算
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = reviews.count()
    
    # Foodテーブルを更新
    food.average_rating = round(average_rating, 1)
    food.total_reviews = total_reviews
    food.save()