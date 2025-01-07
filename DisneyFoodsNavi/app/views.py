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
        print("Rating field choices:", form.fields['rating'].choices)  # 追加
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
    def get(self, request):
        # カテゴリとエリアを選択
        category = request.GET.get('category')
        area = request.GET.get('area')
        
        # カテゴリが数字かチェック
        try:
            category = int(category) if category else None
        except ValueError:
            category = None # 不正な値の場合は　None を設定

        # フィルタリング
        foods = Food.objects.filter(category__kind=category) if category else Food.objects.all()
        stores = Store.objects.filter(area__area_name=area, foodstore__food__in=foods) if area else []
        
        # コンテキストデータを設定
        context = {
            'stores': stores,
            'category': category,
            'area': area,
        }
        return render(request, 'map.html', context)
    
    # def get(self, request):
    #     return self.search_results(request)

    
class MyReviewView(View):
    def get(self, request):
        return render(request, "myreview.html")


