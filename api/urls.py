""" url patterns for transaction api
"""
from django.urls import path
from .views import *

# -------------- ViewSets --------------------------------

# -------------- End --------------------------------

app_name = 'api'
urlpatterns = [
    # main
    path('transfer', transfer, name='transfer'),
    path('fund_wallet', fund_wallet, name='fund_wallet'),
    path('transfer_out', transfer_out, name='transfer_out'),
    # wallet
    path('create_wallet', create_wallet, name='create_wallet'),
    path('all_wallets', all_wallets, name='all_wallets'),
    path('get_wallet/<str:user>', get_wallet, name='get_wallet'),
    path('delete_wallet/<str:user>', delete_wallet, name='delete_wallet'),
    # transaction
    path('transactions', all_transactions, name='transactions'),
    path('transactions/user/<str:user>',
         user_transactions, name='user_transactions'),
    path('transactions/<str:id>', transaction_detail, name='transactions')

]
