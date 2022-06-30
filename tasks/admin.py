from django.contrib import admin

# Register your models here.
from django.apps import apps

models_list = apps.get_app_config('tasks')

for model in models_list.get_models():
	admin.site.register(model)