"""
URL configuration for DisneyFoodsNavi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from app.views import PortfolioView, SignupView, LoginView, HomeView, WriteReviewView, ReadingReviewView, FavoriteView, RankingView, MapView, MyReviewView, FoodSearchView, ReviewDetailView, FavoriteToggleView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PortfolioView.as_view(), name="portfolio"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('home/', HomeView.as_view(), name="home"),
    path('writereview/', WriteReviewView.as_view(), name="writereview"),
    path('readingreview/', ReadingReviewView.as_view(), name="readingreview"),
    path('favorite/', FavoriteView.as_view(), name="favorite"),
    path('ranking/', RankingView.as_view(), name="ranking"),
    path('map/', MapView.as_view(), name="map"),
    path('myreview/', MyReviewView.as_view(), name="myreview"),
    path('search-foods/', FoodSearchView.as_view(), name='search_foods'),
    path('food-search/', FoodSearchView.as_view(), name='food-search'),    
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'), # レビュー詳細画面
    path('favorite/toggle/<int:food_id>/', FavoriteToggleView.as_view(), name='favorite_toggle'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
