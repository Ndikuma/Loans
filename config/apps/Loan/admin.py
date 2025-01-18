from django.contrib import admin

# Register your models here.
from .models import Loan, Wallet, WalletActivity

admin.site.register(Wallet)
admin.site.register(Loan)
admin.site.register(WalletActivity)
