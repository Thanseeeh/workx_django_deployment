from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FreelancerProfile

# Register your models here.

class ProfileAdmin(UserAdmin):
    list_display = ('id','profile_photo', 'about', 'date_of_birth', 'level','city', 'state', 'country', 'year_of_experience', 'age', 'is_registered')
    list_display_links = ('id',)
    ordering = ('id','profile_photo')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(FreelancerProfile, ProfileAdmin)