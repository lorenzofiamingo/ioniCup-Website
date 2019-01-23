from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('skeleton/', include('skeleton.urls')),
    path('team/', include('area_team.urls')),
    path('master/', include('area_master.urls')),
    path('scorekeeper/', include('area_scorekeeper.urls')),
    path('referee/', include('game_referee.urls')),
    path('schedule/', include('game_schedule.urls')),
    path('scoreboard/', include('game_scoreboard.urls')), ]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "IONICUP"
admin.site.site_title = "IONICUP Admin Portal"
admin.site.index_title = "ADMIN AREA"
