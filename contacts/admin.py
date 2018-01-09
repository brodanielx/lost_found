from django.contrib import admin
from contacts.models import Contact, UserProfile

class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'phone_number_formated', 'email', 'added_by', 'created_at', 'updated_at')
    search_fields = ['full_name']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone_number', 'post')
    search_fields = ['user']

admin.site.register(Contact, ContactAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
