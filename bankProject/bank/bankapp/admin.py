
from django.contrib import admin
from .models import CustomUser, BankAccount, Transaction

admin.site.register(CustomUser)
admin.site.register(BankAccount)
admin.site.register(Transaction)
