from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # página principal
    path('dashboard/', include('dashboard.urls')),
    path('visor/', include('visor.urls')),
]