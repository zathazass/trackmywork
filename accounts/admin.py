from django.contrib import admin
from django.apps import apps
from rest_framework_simplejwt import token_blacklist


models_list = apps.get_app_config('accounts')

for model in models_list.get_models():
	admin.site.register(model)


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)