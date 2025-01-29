from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Loan, Wallet


@receiver([post_delete, post_save], sender=Loan)
def handle_loan_cache_clear(sender, instance, created, **kwargs):
    print(" cleaning  loans cache")
    cache.delete_pattern("*loans_list*")


@receiver([post_delete, post_save], sender=Wallet)
def handler_wallet_cache_clear(sender, instance, **kwargs):
    print(" cleaning  wallets cache  ")
    cache.delete_pattern("*wallet_list*")
