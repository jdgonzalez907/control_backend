from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import CustomUser

admin.register(CustomUser, UserAdmin)
