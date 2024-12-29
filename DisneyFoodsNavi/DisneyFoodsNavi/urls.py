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
from app.views import PortfolioView, SignupView, LoginView, HomeView, WriteReviewView, ReadingReviewView, FavoriteView, RankingView, MapView, MyReviewView

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

]
