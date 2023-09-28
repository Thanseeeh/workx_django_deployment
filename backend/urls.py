from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('freelancers/', include('freelancers.urls')),
    path('users/', include('users.urls')),
    path('admin/', include('superadmin.urls')),
    path('', include('chat.urls')),
]