from django.contrib import admin
from .models import MyUser
from typeidea.custom_site import custom_site
# Register your models here.


@admin.register(MyUser,site=custom_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','create_time')
    fields = ('name','email','sex','password')