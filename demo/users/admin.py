from django.contrib import admin
from django.contrib.auth import get_user_model
from uuiduser.admin import UUIDUserAdmin


User = get_user_model()


admin.site.register(User, UUIDUserAdmin)
