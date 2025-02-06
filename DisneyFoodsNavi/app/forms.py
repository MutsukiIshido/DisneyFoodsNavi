from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from app.models import User, Review, ReviewImages, Food, Store
from django.contrib.auth import authenticate
from django.forms import modelformset_factory



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
    class Meta:
        model = Review
        fields = ['food', 'store', 'rating', 'comment']
        widgets = {
            'food': forms.HiddenInput(),  # 明示的に隠しフィールドを設定
        }
        
        
class ReviewImagesForm(forms.ModelForm):
    class Meta:
        model = ReviewImages
        fields = ["review_image_path"]

#　フォームセットを作成（最大５枚の画像をアップロード可能
ReviewImagesFormSet = modelformset_factory(ReviewImages, form=ReviewImagesForm, extra=5, can_delete=True) 
            
# メールアドレスの変更フォーム
class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスはすでに使用されています。")
        return email
    
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'