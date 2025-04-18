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
from django.db.models import Avg, F, Count, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from itertools import groupby
from operator import attrgetter
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import TemplateView




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


class WriteReviewView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = None
    
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
                  
            # 投稿後にレビュー詳細ページへリダイレクト 
            return redirect(reverse("review_detail", kwargs={"pk": review.pk}))
        
        print("❌ フォームのバリデーションエラー:", review_form.errors)
        
        return render(request, "writereview.html", {
            "review_form": review_form,
            "images_form": ReviewImagesForm()  # フォームをリセット
        })

class ReadingReviewView(View):
    def get(self, request):
        request.session['previous_page'] = 'readingreview'

        selected_category = request.GET.get("category")
        selected_food = request.GET.get("food")

        reviews = Review.objects.prefetch_related('images').all()

        if selected_category:
            reviews = reviews.filter(food__category_id=selected_category)
        if selected_food:
            reviews = reviews.filter(food_id=selected_food)

        categories = FoodCategory.objects.all()
        foods = Food.objects.filter(category_id=selected_category) if selected_category else Food.objects.all()

        context = {
            "reviews": reviews,
            "categories": categories,
            "foods": foods,
            "selected_category": selected_category,
            "selected_food": selected_food,
        }
        return render(request, "readingreview.html", context)
    

class FavoriteView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = None
    
    def get(self, request):        
        # ログイン中のユーザーのお気に入りを取得
        favorites = Favorite.objects.filter(user=request.user).select_related('food')
        return render(request, 'favorite.html', {'favorites': favorites})
        
    
class RankingView(View):
    def get(self, request):
        request.session['previous_page'] = 'ranking'
        
        # フードをカテゴリ別に並べて、評価順にソート
        foods = Food.objects.all().select_related('category').order_by('category', '-average_rating')
        
        # カテゴリごとにグループ化して上位3件を抽出
        grouped_foods = {}
        for category, items in groupby(foods, key=attrgetter('category')):
            grouped_foods[category.kind] = list(items)[:3]
        
        is_logged_in = request.user.is_authenticated
        
        favorites = []
        if request.user.is_authenticated:
            favorites = Favorite.objects.filter(user=request.user).values_list('food_id', flat=True)

        return render(request, "ranking.html", {
            'grouped_foods': grouped_foods,
            'is_logged_in': is_logged_in,
            'favorite_food_ids': list(favorites),
        })
    
class MapView(View):
    def get(self, request):
        request.session['previous_page'] = 'map'

        # クエリパラメータ取得
        category_id = request.GET.get('category')
        area = request.GET.get('area')
        price_range_raw = request.GET.get('price_range')  # ← 文字列のまま保存（重要！）
        park = request.GET.get('park')
        food_name = request.GET.get('food_name', '')

        category_name = None
        foods = Food.objects.all()

        # カテゴリで絞り込み
        if category_id:
            try:
                category_obj = FoodCategory.objects.get(id=int(category_id))
                category_name = category_obj.kind
                foods = foods.filter(category=category_obj)
            except (FoodCategory.DoesNotExist, ValueError):
                pass

        # 価格帯フィルター
        if price_range_raw in ["0", "1", "2", "3", "4"]:
            try:
                price_range = int(price_range_raw)  # ← ここだけintにしてフィルター用に使う
                if price_range == 0:
                    foods = foods.filter(price__lte=500)
                elif price_range == 1:
                    foods = foods.filter(price__gt=500, price__lte=1000)
                elif price_range == 2:
                    foods = foods.filter(price__gt=1000, price__lte=1500)
                elif price_range == 3:
                    foods = foods.filter(price__gt=1500, price__lte=2000)
                elif price_range == 4:
                    foods = foods.filter(price__gt=2000)
            except (ValueError, TypeError):
                pass

        # ストアのフィルタ
        stores = Store.objects.filter(foodstore__food__in=foods)

        if area:
            stores = stores.filter(area__area_name=area)

        if park in ["0", "1"]:
            stores = stores.filter(area__park=int(park))

        stores = stores.distinct()

        store_data = []
        for store in stores:
            food_items = FoodStore.objects.filter(store=store)
            for foodstore in food_items:
                food = foodstore.food
                if store.latitude and store.longitude and food:
                    store_data.append({
                        "store_name": store.store_name,
                        "latitude": float(store.latitude),
                        "longitude": float(store.longitude),
                        "food_name": food.foods_name,
                        "category": food.category.kind,
                        "category_id": str(food.category.id),
                        "price": food.price,
                        "area": store.area.area_name if store.area else "",
                        "rating": float(food.average_rating),
                        "food_id": food.id,
                        "park": store.area.park if store.area else "",
                        "image_path": food.foods_image_path if food.foods_image_path else ""
                    })

        context = {
            'stores': store_data,
            'category': str(category_id) if category_id else "",
            'category_name': category_name,
            'area': area,
            'price_range': price_range_raw if price_range_raw else "",  # ← 文字列でテンプレートに渡す！
            'park': park,
            "food_name": food_name
        }

        return render(request, 'map.html', context)


    
class MyReviewView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = None
    
    def get(self, request):
        request.session['previous_page'] = 'myreview'

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
    
    
def get_stores_for_food(request):
    food_id = request.GET.get('food_id')
    stores = []

    if food_id:
        foodstores = FoodStore.objects.filter(food_id=food_id).select_related('store')
        for fs in foodstores:
            stores.append({
                'id': fs.store.id,
                'name': fs.store.store_name
            })

    return JsonResponse(stores, safe=False)

# レビュー一覧画面のカテゴリIDからフード一覧を返すAPI
@require_GET
@csrf_exempt
def get_foods_by_category(request):
    category_id = request.GET.get("category_id")
    if category_id:
        # カテゴリー指定あり：そのカテゴリに属するフードだけ返す
        foods = Food.objects.filter(category_id=category_id).values("id", "foods_name")
    else:
        # カテゴリー指定なし：すべてのフードを返す
        foods = Food.objects.all().values("id", "foods_name")
    return JsonResponse(list(foods), safe=False)
    
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
            favorite = Favorite.objects.filter(user=request.user, food=food).first()
            if favorite:
                favorite.delete()
                message = 'お気に入りから削除しました'
                status = 'removed'
            else:
                Favorite.objects.create(user=request.user, food=food)
                message = 'お気に入りに追加しました'
                status = 'added'

            return JsonResponse({'status': status, 'message': message})

        except Food.DoesNotExist:
            return JsonResponse({'error': '指定されたフードが見つかりません'}, status=404)

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
    template_name = 'password_change.html'  # ★オリジナルテンプレート
    success_url = reverse_lazy('password_change_done')  # ★完了後に飛ばすURL名

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)  # パスワード変更してもログアウトしないため
        messages.success(self.request, "パスワードを変更しました。")  # 成功メッセージ
        return response

# パスワード変更完了画面用ビュー（オリジナル）
class CustomPasswordChangeDoneView(TemplateView):
    template_name = 'password_change_done.html'  # ★オリジナルテンプレート    


class FoodDetailView(View):
    def get(self, request, pk):
        food = get_object_or_404(Food.objects.select_related('category'), pk=pk)
        stores = Store.objects.filter(foodstore__food=food).select_related('area')
        reviews = Review.objects.filter(food=food)
        review_count = reviews.count()
        is_logged_in = request.user.is_authenticated
        
        favorites = []
        if request.user.is_authenticated:
            favorites = Favorite.objects.filter(user=request.user).values_list('food_id', flat=True)

        context = {
            "food": food,
            "stores": stores,
            "reviews": reviews,
            "review_count": review_count,
            "is_logged_in": is_logged_in,
            'favorite_food_ids': list(favorites),
        }
        return render(request, "food_detail.html", context)

from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from app.models import Review

# マイレビュー編集
class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['rating', 'comment']  # 編集できる項目だけ指定
    template_name = 'review_edit.html'
    success_url = reverse_lazy('myreview')  # 更新後はマイレビューに戻す！

    def get_queryset(self):
        # 自分のレビューしか編集できないようにする
        return Review.objects.filter(user=self.request.user)

# マイレビュー削除
class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('myreview')

    def get_queryset(self):
        # 自分のレビューしか削除できないようにする
        return Review.objects.filter(user=self.request.user)

# お気に入り削除用
class FavoriteDeleteView(LoginRequiredMixin, DeleteView):
    model = Favorite
    template_name = 'favorite_confirm_delete.html'  # 確認画面出すなら。出さないなら無視してOK
    success_url = reverse_lazy('favorite')  # 削除後にお気に入り一覧に戻る

    def get_queryset(self):
        # 自分のしか削除できないようにする！
        return Favorite.objects.filter(user=self.request.user)
    

def stores_for_food(request, food_id):
    try:
        food = Food.objects.get(id=food_id)
        stores = food.stores.all()
        data = {
            "stores": [{"id": s.id, "name": s.name} for s in stores]
        }
        return JsonResponse(data)
    except Food.DoesNotExist:
        return JsonResponse({"stores": []})