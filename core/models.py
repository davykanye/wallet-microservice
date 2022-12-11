from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json

# Create your models here.
# NOTE: Write robust models and lots of methods
'''
--------- MODELS ----------------
- WALLETS: email/phone_number, amount, date_created
- TRANSACTION: amount, sender, recipient, date
'''


class WalletManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def find(self, id):
        try:
            int(id)
            wallet = self.get_queryset().get(phone_number=str(id))
        except ValueError:
            wallet = self.get_queryset().get(email=id)

        return wallet


class Wallet(models.Model):
    email = models.EmailField(unique=True,
                              max_length=254, null=True, blank=True)
    phone_number = models.CharField(
        unique=True, max_length=12, null=True, blank=True)
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    objects = models.Manager()
    search_object = WalletManager()

    def __str__(self):
        show = f'{self.id}'
        if self.email != None:
            show = f'{self.email}'
        elif self.phone_number != None:
            show = f'{self.phone_number}'
        else:
            pass
        return show


class Transaction(models.Model):
    amount = models.IntegerField(blank=False, null=False)
    sender = models.CharField(max_length=300, default='sender')
    recipient = models.CharField(max_length=300, default='recipient')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        show = f'{self.sender} -> {self.recipient}'
        return show
