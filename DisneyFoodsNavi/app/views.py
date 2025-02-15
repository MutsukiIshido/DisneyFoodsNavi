import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import SignupForm, LoginForm, ReviewForm, ReviewImagesFormSet, ReviewImagesForm, EmailChangeForm, CustomPasswordChangeForm, modelformset_factory
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from app.models import Food, FoodStore, Store, Area, FoodCategory, Review, ReviewImages, Favorite
from django.db.models import Avg, F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from itertools import groupby
from operator import attrgetter
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse



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
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            # 🔹 ユーザーがどのバックエンドを使用しているか指定
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)

            return redirect("home")
        return render(request, "signup.html", {"form": form})


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
        images_formset = ReviewImagesFormSet(queryset=ReviewImages.objects.none())
        return render(request, "writereview.html", {
            "review_form": review_form,
            "images_formset": images_formset
        })
    
    def post(self, request):
        print("🚀 受け取ったデータ:", request.POST)  
        
        review_form = ReviewForm(request.POST)
        
        if review_form.is_valid():
            print("✅ フォームは正常です！")

            # レビューを保存
            review = review_form.save(commit=False)
            review.user = request.user # ログインユーザーを紐付け
            review.save()
            
            # 画像フォームセットを処理
            images_formset = ReviewImagesFormSet(request.POST, request.FILES, queryset=ReviewImages.objects.none())
            
            if images_formset.is_valid():
                for form in images_formset:
                    if form.cleaned_data.get("review_image_path"):
                        image = form.save(commit=False)
                        image.review = review
                        image.save()
                        
            return redirect("home")
        
        print("❌ フォームのバリデーションエラー:", review_form.errors)
        
        return render(request, "writereview.html", {
            "review_form": review_form,
            "images_form": ReviewImagesForm()  # フォームをリセット
        })



    
class ReadingReviewView(View):
    def get(self, request):
        reviews = Review.objects.prefetch_related('images').all() # DBから全レビューを取得、一緒に画像も取得
        return render(request, 'readingreview.html', {'reviews': reviews})
    

class FavoriteView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login') # ログインしていない場合はログイン画面にリダイレクト
        
        # ログイン中のユーザーのお気に入りを取得
        favorites = Favorite.objects.filter(user=request.user).select_related('food')
        return render(request, 'favorite.html', {'favorites': favorites})
        
    
class RankingView(View):
    def get(self, request):
        # フードをカテゴリ別に並べて、評価順にソート
        foods = Food.objects.all().select_related('category').order_by('category', '-average_rating')
        
        # カテゴリごとにグループ化して上位3件を抽出
        grouped_foods = {}
        for category, items in groupby(foods, key=attrgetter('category')):
            grouped_foods[category.kind] = list(items)[:3]
        
        return render(request, "ranking.html", {'grouped_foods': grouped_foods})
    
    
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
        foods = Food.objects.filter(category__id=category) if category else Food.objects.all()
        stores = Store.objects.filter(area__area_name=area, foodstore__food__in=foods).distinct() if area else Store.objects.all()
        
        # デバッグ用にデータをサーバーログに出力
        print("Filtered Stores:", stores)
        
        # クエリセットを辞書リストに変換（JSONに変換しやすくする）
        store_data = []
        for store in stores:
            food_items = FoodStore.objects.filter(store=store)  # ManyToManyFieldの場合
            for foodstore in food_items:
                if store.latitude and store.longitude:
                    store_data.append({
                        "store_name": store.store_name,
                        "latitude": float(store.latitude),
                        "longitude": float(store.longitude),
                        "food_name": foodstore.food.foods_name if foodstore.food else "不明",
                        "category": foodstore.food.category.kind if foodstore else None,  # カテゴリ情報を追加
                        "price": foodstore.food.price if foodstore.food else "不明",
                        "area": store.area.area_name if store.area else None,  # エリア情報を追加
                        "rating": float(foodstore.food.average_rating) if foodstore.food else "0"
                    })
                    
        print("", store_data)  # ログ確認用

        
        # コンテキストデータを設定
        context = {
            'stores': store_data,
            'category': category,
            'area': area,
        }
        return render(request, 'map.html', context)
    
        # ビュー内でデータの確認
        print("JSON Store data:", store_data)  # サーバーコンソールに表示



    
class MyReviewView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login') # ログインしていない場合はログイン画面にリダイレクト

        # ログイン中のユーザーのレビューを取得
        reviews = Review.objects.filter(user=request.user).prefetch_related('images')

        breadcrumbs = [
            {"name": "ホーム", "url": "/home/"},
            {"name": "マイレビュー一覧", "url": "/myreview/"}
            ]

        return render(request, 'myreview.html', {
            'reviews': reviews,
            'breadcrumbs': breadcrumbs
        })
        
class FoodSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if query:
            foods = Food.objects.filter(foods_name__icontains=query).values('id', 'foods_name')
            results = [{'id': food['id'], 'name': food['foods_name']} for food in foods]
        else:
            results = []
        return JsonResponse(results, safe=False)
    
# レビュー詳細画面用ビュー
class ReviewDetailView(View):
    def get(self, request, pk):
        try:
            pk = int(pk) # URLから渡されたpkを整数型に変換
        except ValueError:
            return JsonResponse({'error': 'Invalid pk value'}, status=400)
        
        # レビューを取得
        review = get_object_or_404(Review.objects.select_related('food', 'store'), pk=pk)
        
        # パンくずリストを修正
        breadcrumbs = []
        breadcrumbs.append({"name": "ホーム", "url": reverse('home')})
        
        # 遷移元URL(HTTP_REFERER)を取得
        referer = request.META.get('HTTP_REFERER', '')
        
        # 遷移元がレビュー一覧またはマイレビューの場合、対応するパンくずを追加
        if 'readingreview' in referer:
            breadcrumbs.append({"name": "レビュー一覧", "url": "/readingreview/"})
        elif 'myreview' in referer:
            breadcrumbs.append({"name": "マイレビュー", "url": "/myreview/"})
            
        # 現在のページ（レビュー詳細）を追加
        breadcrumbs.append({"name": "レビュー詳細", "url": "request.path"})
        
        # パンくずリストとレビューをテンプレートに渡してレンダリング        
        return render(request, 'review_detail.html', {
            'breadcrumbs': breadcrumbs,
            'review': review
        })


# お気に入りの登録・削除機能
@method_decorator(login_required, name='dispatch')
class FavoriteToggleView(View):
    def post(self, request, food_id):
        try:
            food = Food.objects.get(id=food_id)
            
            # お気に入り登録
            favorite, created = Favorite.objects.get_or_create(user=request.user, food=food)
            if created:
                message = 'お気に入りに追加しました'
                status = 'added'
            else:
                favorite.delete()
                message = 'お気に入りから削除しました'
                status = 'removed'
            return JsonResponse({'status': status, 'message': message}, status=200)
        
        except Food.DoesNotExist:
            return JsonResponse({'error': '指定されたフードが見つかりません'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
# メールアドレス変更用ビュー
class EmailChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = EmailChangeForm(instance=request.user)
        return render(request, 'email_change.html', {'form': form})
    
    def post(self, request):
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "メールアドレスを変更しました。")
            return redirect('home')
        return render(request, 'email_change.html', {'form': form})

# パスワード変更用ビュー 
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "password_change.html"
    success_url = reverse_lazy('password_change_done')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user) # セッションのハッシュを更新
        messages.success(self.request, "パスワードを変更しました。")
        return response