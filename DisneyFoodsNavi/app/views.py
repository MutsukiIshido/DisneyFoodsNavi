from django.shortcuts import render, redirect
from django.views import View
from app.forms import SignupForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return render(request, "writereview.html")
    
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
        return render(request, "map.html")
    
class MyReviewView(View):
    def get(self, request):
        return render(request, "myreview.html")