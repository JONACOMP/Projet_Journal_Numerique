from django.contrib import admin
from Accounts import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    model = models.User
    list_display = [
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
        "date_joined",
        "last_updated",
        "bio",
        "profile_picture",
    ]


