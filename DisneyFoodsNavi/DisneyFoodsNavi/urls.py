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
from app.views import PortfolioView, SignupView, LoginView, HomeView, WriteReviewView, ReadingReviewView, FavoriteView, RankingView, MapView, MyReviewView, FoodSearchView, ReviewDetailView, FavoriteToggleView, EmailChangeView, PasswordChangeView, get_stores_for_food, FoodDetailView, get_foods_by_category, ReviewUpdateView, ReviewDeleteView, FavoriteDeleteView, CustomPasswordChangeView, CustomPasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeDoneView, LogoutView

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
    path('food-search/', FoodSearchView.as_view(), name='food-search'),    
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'), # レビュー詳細画面
    path('favorite/toggle/<int:food_id>/', FavoriteToggleView.as_view(), name='favorite_toggle'),
    path('email_change/', EmailChangeView.as_view(), name='email_change'),    
    path('logout/', LogoutView.as_view(), name='logout'),
    path("api/get-stores-for-food/", get_stores_for_food, name="get_stores_for_food"),
    path('food/<int:pk>/', FoodDetailView.as_view(), name='food_detail'),
    path('api/foods_by_category/', get_foods_by_category, name='foods_by_category'),
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('favorite/delete/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite_delete'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)