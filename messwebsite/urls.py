from django.contrib import admin
from django.urls import path, include
from allauth.account.views import logout, signup
from allauth.socialaccount.providers.google.views import oauth2_login, oauth2_callback
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include('home.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('accounts/google/login/', oauth2_login, name="google_login"),
    # path('accounts/google/login/callback/', oauth2_callback, name="google_callback"),
    path('account/', include('allauth.socialaccount.urls')),
    path('ajax/', include('ajax.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
