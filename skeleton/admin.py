from django.contrib import admin
from .models import *


class PlayerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tournament)
admin.site.register(AllStarGame)
admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Coach)
admin.site.register(Stage)
admin.site.register(Group)
admin.site.register(Round)
admin.site.register(Match)
admin.site.register(Score)
admin.site.register(Court)
admin.site.register(Day)
admin.site.register(Time)
