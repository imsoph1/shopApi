from django.contrib import admin

from account.models import CustomUser, Spam_Contacts

admin.site.register(CustomUser)
admin.site.register(Spam_Contacts)
