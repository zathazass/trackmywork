from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import (
    authenticate, login as django_login, logout as django_logout,
    get_user_model
)

from trackmywork.utilities.funcs import generate_otp
from .forms import *
from .selectors import get_user
from .services import create_account_confirmation, create_user, check_and_update_account_confirmation, create_user_secret

from trackmywork.config.base import KEEP_ME_SESSION_TIME, EMAIL_HOST_USER

User = get_user_model()

def login_page(request):
    z = False
    if request.user.is_authenticated: django_logout(request)
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        keep_me = True if request.POST.get('keep_me', None) == 'on' else False
        if z: print(keep_me)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = get_user(username)
            if isinstance(user, ObjectDoesNotExist):
                form.add_error(error='User does not exist', field='username')
            elif user:
                if not user.active:
                    form.add_error(error='Account Confirmation is required',field='__all__')
                if hasattr(user, 'accountstatus'):
                    form.add_error(error=user.accountstatus.description, field='__all__')
            
                if not form.errors:
                    valid_user = authenticate(username=user.username, password=password)
                    if valid_user:
                        if keep_me: request.session.set_expiry(KEEP_ME_SESSION_TIME)
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
    z = True
    if request.user.is_authenticated: django_logout(request)
    form = RegisterForm()
    context = {'created': False, 'form': form}
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
            form.cleaned_data['is_active'] = True
            if z: print('form valid', form.cleaned_data, 'view')
            user = create_user(**form.cleaned_data)
            otp = generate_otp()
            acc_conf = create_account_confirmation(user=user, otp=otp)
            if z: print(acc_conf.otp)
            us = create_user_secret(user)
            if z: print(us.unique_key)
            
            try:
                email = EmailMessage(subject='Account Confirmation OTP : Track My Work',
                body=f'''
                Hi {request.user.username}, your account confirmation otp is {otp}, expired in 60 minutes
                ''', from_email=EMAIL_HOST_USER, to=[user.email])
                email.send()
            except Exception as e:
                user.is_active = True
                user.save()
                if z: print(e) # [Errno 111] Connection refused
            form = RegisterForm()
            context.update({'form': form, 'created': True, 'key': us.unique_key})
        else:
            context.update({'created': False, 'form': form})
            if z: print('invalid form', form.errors, 'view')
    
    return render(request, 'accounts/register.html', context=context)


def check_username(request):
    z = False
    if request.method == 'POST' and request.is_ajax():
        user = get_user(request.POST['username'])
        if isinstance(user, ObjectDoesNotExist):
            status = True
            if z: print('hi')
        elif isinstance(user, User):
            status = False
            if z: print('hello')
        
        return JsonResponse(data={'success': status}, status=200)
    elif request.method == 'GET':
        return JsonResponse(data={'message': 'only allow post method'})


def account_confirmation_page(request):
    z = False
    form = AccountConfirmationForm()
    if request.method == 'POST':
        form = AccountConfirmationForm(request.POST)
        if form.is_valid():
            if z: print(form, 'valid')
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']
            acc_conf = check_and_update_account_confirmation(email=email, otp=otp)
            if acc_conf == 'confirm':
                messages.info(request, 'Your account has been confirmed')
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
            if z: print(form.errors, 'invalid')

    context = {'form': form}
    return render(request, 'accounts/confirm.html', context)


def forgot_password_page(request):
    return render(request, 'accounts/forgot-password.html')


def send_otp(request):
    '''Password Reset Email OTP'''
    z = False
    if request.method == 'GET':
        return JsonResponse('only allow POST method')
    if request.method == 'POST':
        if z: print(request.POST)
        user = get_user(request.POST.get('username', ''))
        if isinstance(user, ObjectDoesNotExist):
            return JsonResponse(data={'success':False,'message': 'Username or Email does not exist'})
        
        ac_obj = AccountConfirmation.objects.get(user=user)
        ac_obj.otp = generate_otp()
        ac_obj.save()
        otp = ac_obj.otp
        print('OTP is sending ...', otp)
        try:
            email = EmailMessage(subject='Password Reset OTP : Track My Work',
            body=f'''
            Hi {request.user.username}, your password reset otp is {otp}, expired in 60 minutes
            ''', from_email=EMAIL_HOST_USER, to=[user.email])
            email.send()
            return JsonResponse(data={'success': False, 'message': 'Found Error in sending email, please choose "try another way"'})
        except Exception as e:
            if z: print(e)
        return JsonResponse(data={'success': True, 'message': 'password reset confirmation otp sent successfully to your email.'})


def confirm_otp(request):
    '''Password Reset Confirmation OTP'''
    if request.method == 'GET': return JsonResponse(data='only allow POST method', safe=False)
    if request.method == 'POST':
        otp = request.POST['otp']
        email = request.POST['email']
        try:
            ac_obj = AccountConfirmation.objects.get(user__email=email, otp=otp)
            return JsonResponse(data={'success': True, 'message': 'OTP Verified'})
        except AccountConfirmation.DoesNotExist:
            return JsonResponse(data={'success': False, 'message': 'Invalid OTP'})


def get_unique_key(request):
    z = False
    if request.method == 'GET':
        return JsonResponse('only allow POST method')
    if request.method == 'POST':
        status = False
        key = request.POST.get('key', '')
        email = request.POST.get('email', '')
        if z: print(key, email, 'key email')
        if key and email:
            try:
                u = UserSecret.objects.get(user__email=email, unique_key=key)
                if u: status = True
            except UserSecret.DoesNotExist:
                status = False
        return JsonResponse(data={'success': status})


def reset_password(request):
    if request.method == 'GET':
        return JsonResponse('only allow POST method')
    if request.method == 'POST':
        email = request.POST.get('email', '')
        key_or_otp = request.POST.get('key_or_otp', '')
        p1 = request.POST.get('password', '')
        p2 = request.POST.get('confirm_password', '')

        if p1 != p2:
            return JsonResponse(data={
                'status': 'error', 'message': 'Password and Confirm password does not match'})
        if len(key_or_otp) == 6:
            try:
                AccountConfirmation.objects.get(user__email=email, otp=key_or_otp)
            except AccountConfirmation.DoesNotExist:
                return JsonResponse(data={'status': 'error', 'message': 'Invalid OTP'})
        else:
            try:
                UserSecret.objects.get(user__email=email, unique_key=key_or_otp)
            except UserSecret.DoesNotExist:
                return JsonResponse(data={'status': 'error', 'message': 'Invalid Unique Key'})

        user = User.objects.get(email=email)
        user.set_password(p1)
        user.save()
        messages.info(request, 'password reset completed successfully')
        return JsonResponse(data={'status': 'success'})


def terms_page(request):
    return render(request, 'policies/terms-and-conditions.html')