import logging
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import AccountConfirmation


logger = logging.getLogger('common')

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def create_user(*, username, password, email, accept_terms_and_conditions, is_active):
    user = User(
        username=username, email=email, is_active=is_active,
        accept_terms_and_conditions=accept_terms_and_conditions
    )
    user.set_password(password)
    user.full_clean()
    user.save()
    return user


def update_user(ins, **kwargs):
    for key, value in kwargs.items():
        setattr(ins, key, value)
    ins.full_clean()
    ins.save()

def create_account_confirmation(*, user, otp):
    acc_conf = AccountConfirmation(
        user=user, otp=otp
    )
    acc_conf.full_clean()
    acc_conf.save()
    return acc_conf


def update_account_confirmation(*, email, otp):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return 'not_found'

    try:
        acc_conf = AccountConfirmation.objects.get(user__email=email)
    except AccountConfirmation.DoesNotExist as e:
        logger.error('Account Confirmation Object not created', e)
        return 'error'

    except MultipleObjectsReturned as e:
        logger.critical('Found More than one Account Confirmation Object', e)
        return 'error'
    
    if acc_conf.otp == otp:
        if not acc_conf.is_expired():
            acc_conf.confirmation_status = True
            acc_conf.save()
            update_user(user, is_active=True)
            return 'confirm'
        else:
            return 'expired'
    else:
        return 'invalid'