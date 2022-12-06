from django.db import models
import json

# Create your models here.
# NOTE: Write robust models and lots of methods
'''
--------- MODELS ----------------
- WALLETS: email/phone_number, amount, date_created
- TRANSACTION: amount, sender, recipient, date
'''


class Wallet(models.Model):
    email = models.EmailField(
        max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        show = f'{self.id}'
        if self.email != None:
            show = f'{self.email}'
        elif self.phone_number != None:
            show = f'{self.phone}'
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
