from django.contrib import admin
from django.contrib.auth.models import User

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_staff')