from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import MyUser, Cart

class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False
    verbose_name_plural = "MyUser"


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Cart)