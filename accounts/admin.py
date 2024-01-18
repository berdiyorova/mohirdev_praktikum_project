from django.contrib import admin
from .models import Profile

# Register your models here.
# 1-usul
#
# admin.site.register(Profile)


# 2-usul

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

admin.site.register(Profile, ProfileAdmin)
