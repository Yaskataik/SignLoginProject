from django.contrib import admin
from django.urls import path, include  # <-- We added 'include' here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')), # <-- We added this bridge line
]