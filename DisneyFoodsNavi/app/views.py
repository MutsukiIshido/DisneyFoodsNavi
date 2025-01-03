from django.shortcuts import render, redirect
from django.views import View
from app.forms import SignupForm, LoginForm, ReviewForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Food, FoodStore, Store, Area, FoodCategory, Review
from django.db.models import Avg


class PortfolioView(View):
    def get(self, request):
        return render(request, "portfolio.html")
    
    
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", context={
            "form":form
        })
    def post(self, request):
        print(request.POST)
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, "signup.html", context={
            "form":form
        })


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("home")
        return render(request, "login.html", context={
            "form":form
        })

    
class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class WriteReviewView(View):
    def get(self, request):
        form = ReviewForm()
        return render(request, "writereview.html", {"form": form})
    
    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid:
            review = form.save(commit=False)
            review.user = request.user # ログインしているユーザーを設定
            review.save()
        else:
            print(form.errors) # フォームエラーを出力してデバッグ
            return redirect("home") # 投稿後にホームページにレダイレクト
        return render(request, "writeview.html", {"form": form})

    
class ReadingReviewView(View):
    def get(self, request):
        return render(request, "readingreview.html")
    

class FavoriteView(View):
    def get(self, request):
        return render(request, "favorite.html")

    
class RankingView(View):
    def get(self, request):
        return render(request, "ranking.html")    

    
class MapView(View):
    def search_results(self, request):
        category = request.GET.get('category')
        area_name = request.GET.get('area')
        
        try:
            category = int(request.GET.get('category')) # categoryを正数に変換
        except (ValueError, TypeError):
            category = None # 不正な値の場合は　None を設定

        # フードとストアを条件に基づいてフィルタリング
        foods = FoodCategory.objects.filter(kind=category).values_list('food', flat=True)
        stores = Store.objects.filter(area__area_name=area_name, foodstore__food_id__in=foods)

        context = {
            'stores': stores,
            'category': category,
            'area': area_name,
        }
        return render(request, 'map.html', context)
    
    def get(self, request):
        return self.search_results(request)

    
class MyReviewView(View):
    def get(self, request):
        return render(request, "myreview.html")


