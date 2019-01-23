from django.db import models
from django.contrib.auth.models import AbstractUser
from skeleton.models import Team


class IoniUser(AbstractUser):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, default=None)
    is_scorekeeper = models.BooleanField(default=False)
    is_master = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'IoniUser'
        # verbose_name_plural = 'My images'
