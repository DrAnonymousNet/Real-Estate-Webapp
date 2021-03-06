
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account.views import login_view, logout_view,register_view, profile_create

urlpatterns = [
    path('', include('realEstate.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('login/',login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    path('profile/', profile_create, name="profile"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



