from django.contrib import admin
from contacts.models import Contact, UserProfile

class ContactAdmin(admin.ModelAdmin):
    list_display = ('gender', 'full_name', 'phone_number', 'email', 'added_by')
    search_fields = ['full_name']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('gender','user')
    search_fields = ['user']

admin.site.register(Contact, ContactAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
