from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login

from .forms import *
from .selectors import get_user


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = get_user(username)
            if isinstance(user, ObjectDoesNotExist):
                form.add_error(error='User does not exist', field='username')
            elif user:
                valid_user = authenticate(username=user.username, password=password)
                if valid_user:
                    django_login(request, valid_user)
                    return redirect('accounts:home_page')
                else:
                    form.add_error(error='Password is incorrect', field='password')

    context = {'form': form}
    return render(request, 'accounts/login.html', context)

@login_required
def home_page(request):
    return render(request, 'accounts/home.html')