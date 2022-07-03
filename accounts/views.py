from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def login_page(request):
    return render(request, 'accounts/login.html')

@login_required
def home_page(request):
    return render(request, 'accounts/home.html')