from django.shortcuts import render
# rest_framework imports
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
# from rest_framework import viewsets
from rest_framework.response import Response
# Other dependencies
from core.models import Wallet, Transaction
from core.serializers import WalletSerializer, TransactionSerializer
# Create your views here.
'''
------- WALLETS ---------------
- CRUD wallet
- Transfer || wallet -> wallet *
- Fund wallet account -> wallet *
- Transfer || wallet -> account *
-------- TRANSACTIONS ---------------
- CRUD Transaction
- fetch all transactions
- fetch user transactions

'''

# ---------------- WALLET VIEWS --------------------------------


@api_view(['POST'])
def transfer(request):
    pass


@api_view(['POST'])
def fund_wallet(request):
    pass


@api_view(['POST'])
def transfer_out(request):
    pass

# ---------------- TRANSACTION VIEWS --------------------------------


@api_view(['GET'])
def user_transactions(request, id):
    pass

# ---------------- CRUD VIEWS --------------------------------


class WalletViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing wallets.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing transactions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
