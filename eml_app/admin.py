# eml_app/admin.py
from django.contrib import admin
from .models import UserDetail

@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'mobile', 'gender', 'location', 'occupation', 'email', 'created_at')
    search_fields = ('name', 'email', 'mobile')
    list_filter = ('gender', 'location')
