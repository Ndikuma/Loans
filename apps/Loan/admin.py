from django.contrib import admin

# Register your models here.
from .models import Loan, Wallet

admin.site.register(Wallet)
admin.site.register(Loan)
