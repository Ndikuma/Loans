from django.contrib import admin

from .models import Role, User

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
