from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import SignupForm, LoginForm, ReviewForm, ReviewImagesForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Food, FoodStore, Store, Area, FoodCategory, Review, ReviewImages
from django.db.models import Avg
from django.http import JsonResponse


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
        review_form = ReviewForm()
        images_form = ReviewImagesForm()
        return render(request, "writereview.html", {
            "review_form": review_form,
            "images_form": images_form
        })
    
    def post(self, request):
        review_form = ReviewForm(request.POST)
        images_form = ReviewImagesForm(request.POST, request.FILES)
        
        if review_form.is_valid():
            # レビューを保存
            review = review_form.save(commit=False)
            review.user = request.user # ログインユーザーを紐付け
            review.save()
            
            # 複数画像を保存
            if images_form.is_valid():
                images_form.save(review=review)  # ReviewImagesFormのsaveメソッドを呼び出す
            
            return redirect("home")
        
        return render(request, "writereview.html", {
            "review_form": review_form,
            "images_form": images_form     
        })

    
class ReadingReviewView(View):
    def get(self, request):
        reviews = Review.objects.prefetch_related('images').all() # DBから全レビューを取得、一緒に画像も取得
        return render(request, 'readingreview.html', {'reviews': reviews})
    

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

class FoodSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if query:
            foods = Food.objects.filter(foods_name__icontains=query).values('id', 'foods_name')
            results = [{'id': food['id'], 'name': food['foods_name']} for food in foods]
        else:
            results = []
        return JsonResponse(results, safe=False)
    

class ReviewDetailView(View):
    def get(self, request, pk):
        # `select_related`を使用して関連オブジェクトを取得
        review = get_object_or_404(Review.objects.select_related('food', 'store'), pk=pk) # レビューを取得
        return render(request, 'review_detail.html', {'review': review})
