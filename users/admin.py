from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):

    """Custom User Model"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "account_id",
                    "avatar",
                    "superhost",
                    "login_method",
                    "fav_posts",
                )
            },
        ),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
        "fav_posts",
    )
