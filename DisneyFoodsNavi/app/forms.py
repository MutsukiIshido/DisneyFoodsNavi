from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User, Review, ReviewImages, Food, Store
from django.contrib.auth import authenticate


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["nickname", "email", "password1", "password2"]
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスはすでに登録されています")
        return email
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    
    
    def clean(self):
        print("ログインフォームのcleanが呼び出された")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        print(email, password)
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            raise forms.ValidationError("認証に失敗しました")
        return self.cleaned_data
    
    
class ReviewForm(forms.ModelForm):
    food = forms.ModelChoiceField(
        queryset=Food.objects.all(),
        widget=forms.HiddenInput(), # 商品名を非表示フィールドに変更
        label="商品名"
    )
    
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="利用した店舗"
    )
    
    rating = forms.ChoiceField(
        choices=Review.SCORE_CHOICES,
        widget=forms.RadioSelect,
        initial=3,
        label="評価"
    )
    
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="レビュー"
    )
    
    class Meta:
        model = Review
        fields = ['food', 'store', 'rating', 'comment']
        
        
class ReviewImagesForm(forms.Form):
    review_image_path = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        label="画像",
        required=False,
    )