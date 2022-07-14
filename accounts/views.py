from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate, login as django_login, logout as django_logout,
    get_user_model
)

from trackmywork.utilities.funcs import generate_otp
from .forms import *
from .selectors import get_user
from .services import create_account_confirmation, create_user, update_account_confirmation


User = get_user_model()

def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = get_user(username)
            if isinstance(user, ObjectDoesNotExist):
                form.add_error(error='User does not exist', field='username')
            elif user:
                if not user.active:
                    form.add_error(error='Account Confirmation is required',field='__all__')
                if user.status == False:
                    form.add_error(error=user.accountstatus.description, field='__all__')
            
                if not form.errors:
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


@login_required
def logout_view(request):
    django_logout(request)
    messages.info(request, 'Successfully logged out')
    return redirect('accounts:login_page')


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        requested_data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'confirm_password': request.POST.get('confirm_password'),
            'email': request.POST.get('email'),
            'accept_terms_and_conditions': request.POST.get('terms', False)
        }
        form = RegisterForm(data=requested_data)
        if form.is_valid():
            form.cleaned_data.pop('confirm_password')
            form.cleaned_data['is_active'] = False
            print('form valid', form.cleaned_data, 'view')
            user = create_user(**form.cleaned_data)
            acc_conf = create_account_confirmation(user=user, otp=generate_otp())
            print(acc_conf.otp)
            return redirect('accounts:account_confirmation_page')
        else:
            print('invalid form', form.errors, 'view')

    context = {'form': form}
    return render(request, 'accounts/register.html', context=context)


def check_username(request):
    if request.method == 'POST' and request.is_ajax():
        user = get_user(request.POST['username'])
        if isinstance(user, ObjectDoesNotExist):
            status = True
            print('hi')
        elif isinstance(user, User):
            status = False
            print('hello')
        
        return JsonResponse(data={'success': status}, status=200)
    elif request.method == 'GET':
        return JsonResponse(data={'message': 'only allow post method'})


def account_confirmation_page(request):
    form = AccountConfirmationForm()
    if request.method == 'POST':
        form = AccountConfirmationForm(request.POST)
        if form.is_valid():
            print(form, 'valid')
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']
            acc_conf = update_account_confirmation(email=email, otp=otp)
            if acc_conf == 'confirm':
                return redirect('accounts:login_page')
            if acc_conf == 'not_found':
                form.add_error(error='email is does not match with user', field='email')
            if acc_conf == 'expired':
                form.add_error(error='OTP is expired, kindly click resend otp', field='__all__')
            if acc_conf == 'invalid':
                form.add_error(error='invalid otp try again', field='otp')
            if acc_conf == 'error':
                form.add_error(error='technical issue contact admin', field='__all__')
        else:
            print(form.errors, 'invalid')

    context = {'form': form}
    return render(request, 'accounts/confirm.html', context)