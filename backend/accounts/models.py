from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from trackmywork.utilities.model_fields import ConfidentialField


class UserManager(BaseUserManager):
    def create_user(self, username=None, password=None, email=None, is_active=True):
        # Checking user entered valid data
        if not username:
            raise ValueError('User must have username')
        if not password:
            raise ValueError('User must have password')
        if not email:
            raise ValueError('User must have email')

        # Instantiate and save user data
        user = self.model(
            username=username, email=self.normalize_email(email), is_active=is_active
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff_user(self, username=None, password=None, email=None, is_active=True):
        user = self.create_user(
            username=username, email=email, password=password, is_active=is_active
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, password=None, email=None, is_active=True):
        user = self.create_user(
            username=username, email=email, password=password, is_active=is_active
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=64, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # password & last_login fields auto-injected by django BaseUser model

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['created_at']

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username} - {self.email}'

    @property
    def active(self):
        return self.is_active

    @property
    def staff(self):
        return self.is_staff

    @property
    def admin(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class AccountConfirmation(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    confirmation_status = models.BooleanField(default=False)

    def __str__(self):
        if self.confirmation_status:
            return f'{self.user.email} - Account Confirmed'
        return f'{self.user.email} - Account not Confirmed'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=64)
    mobile = ConfidentialField()

    def __str__(self):
        return f'{self.user.username} - {self.user.email}'
