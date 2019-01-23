from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import IoniUser


class IoniUserCreationForm(UserCreationForm):

    class Meta:
        model = IoniUser
        fields = ('username', )


class IoniUserChangeForm(UserChangeForm):

    class Meta:
        model = IoniUser
        fields = ('username', 'email',  'team', )
