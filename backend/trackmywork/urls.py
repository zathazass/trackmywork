from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>You cannot use backend directly</h1>')


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
]
