from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static


def index_page(request):
    return render(request, 'index.html')


urlpatterns = [
    path('', index_page, name='index_page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('__reload__/', include('django_browser_reload.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
