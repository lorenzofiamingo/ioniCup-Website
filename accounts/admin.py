from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import IoniUserCreationForm, IoniUserChangeForm
from .models import IoniUser


class IoniUserAdmin(UserAdmin):
    add_form = IoniUserCreationForm
    form = IoniUserChangeForm
    model = IoniUser
    list_display = ['username', 'email',  'team', ]

    fieldsets = (
            (None, {
                'fields': ('team',)
            }),
    ) + UserAdmin.fieldsets

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'team'),
        }),
    )


admin.site.register(IoniUser, IoniUserAdmin)
