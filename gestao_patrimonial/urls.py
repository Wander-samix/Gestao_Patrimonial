from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # raiz → login
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),

    # admin
    path('admin/', admin.site.urls),

    # mounta TUDO (web + API) a partir de interface/urls.py
    path('', include('interface.urls')),
]
