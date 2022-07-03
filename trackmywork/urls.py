from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static


def index(request):
    return HttpResponse('<h1>You cannot use backend directly</h1>')


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('__reload__/', include('django_browser_reload.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
