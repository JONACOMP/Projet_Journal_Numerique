from django.apps import apps
from django.contrib import admin

# Register your models here.

app_models = apps.get_app_config('notebook').get_models()
for model in app_models:
    try:    

        admin.site.register(model)

    except Exception:
        pass