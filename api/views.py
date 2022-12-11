from django.shortcuts import render
# rest_framework imports
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
# from rest_framework import viewsets
from rest_framework.response import Response
# Other dependencies
from core.models import Wallet, Transaction
from core.serializers import WalletSerializer, TransactionSerializer
from utils.transfer import Transfer

# Create your views here.
'''
------- WALLETS ---------------
- CRUD wallet ✓
- Transfer || wallet -> wallet * ✓
- Fund wallet account -> wallet * ✓
- Transfer || wallet -> account *
-------- TRANSACTIONS ---------------
- CRUD Transaction ✓
- fetch user transactions ✓

'''

# TODO: Handle Exceptions Properly
# TODO: Build Custom Exception Handler
# ---------------- MAIN VIEWS --------------------------------


@api_view(['POST'])
def transfer(request):
    '''
    - ### **METHOD**: POST
    - ### **DESCRIPTION**: Transfer between two user wallets
    - ### **EXAMPLE**: {"amount":20, "sender":"example@gmail.com", "recipient":"08127088448"}
    '''
    try:
        # instantiate all objects
        amount = request.data['amount']
        # tip = Wallet.objects.all()
        sender = Wallet.search_object.find(request.data['sender'])
        recipient = Wallet.search_object.find(request.data['recipient'])
        # print(sender, recipient, tip)
        # Move the money
        sender.amount -= int(amount)
        recipient.amount += int(amount)
        sender.full_clean()
        sender.save()
        recipient.full_clean()
        recipient.save()
        # Create transaction
        transaction = Transaction.objects.create(amount=int(
            amount), sender=request.data['sender'], recipient=request.data['recipient'])
        transaction.save()

        data = TransactionSerializer(transaction, many=False)
        return Response(data.data)
    except Exception as e:
        return Response(
            {
                'error': 'An error occurred',
                'exception': str(e)
            },
            exception=True
        )


@api_view(['POST'])
def fund_wallet(request):
    '''
    - ### **METHOD**: POST
    - ### **DESCRIPTION**: Funding user wallet after gateway payment
    - ### **EXAMPLE**: {"user": "davykanye@gmail.com", "amount": 20}
    '''
    try:
        amount = request.data['amount']
        wallet = Wallet.search_object.find(request.data['user'])
        wallet.amount += abs(amount)
        wallet.full_clean()
        wallet.save()

        data = {'Message': f'Wallet funded Successfully, {amount} added',
                'amount': wallet.amount}
        return Response(data)
    except Exception as e:
        return Response(
            {
                'error': 'An error occurred',
                'exception': str(e)
            },
            exception=True
        )

# TODO:Solve bank name input problem


@api_view(['POST'])
def transfer_out(request):
    '''
    - ### **METHOD**: POST
    - ### **DESCRIPTION**: Transfer to External Bank Account
    - ### **EXAMPLE**: {"amount":20, "account": {"account_number": "2018219672", "bank_name": "Kuda Bank"}}
    '''
    try:
        account_data = request.data['account']
        paystack = Transfer('Test transfer')
        recipient = paystack._create_recipient(
            account_data)[3]['recipient_code']
        # print("Data is", recipient)
        paystack._set_recipient(recipient)
        paystack._transfer(int(request.data['amount']*100))

        return Response(f"{request.data['amount']} transfered successfully to {account_data['account_number']}")
    except Exception as e:
        return Response(
            {
                'error': 'An error occurred',
                'exception': str(e)
            },
            exception=True
        )
# ---------------- TRANSACTION VIEWS --------------------------------


@api_view(['GET'])
def all_transactions(request):
    query = Transaction.objects.all()
    serializer = TransactionSerializer(query, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def transaction_detail(request, id):
    try:
        query = Transaction.objects.get(id=id)
        serializer = TransactionSerializer(query, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {
                'error': 'An error occurred',
                'exception': str(e)
            },
            exception=True
        )


@api_view(['GET'])
def user_transactions(request, user):
    try:
        t1 = Transaction.objects.filter(sender=user)
        t2 = Transaction.objects.filter(recipient=user)
        user_transactions = t1 | t2
        data = TransactionSerializer(user_transactions, many=True)
        return Response(data.data)
    except Exception as e:
        return Response(
            {
                'error': 'An error occurred',
                'exception': str(e)
            },
            exception=True
        )

# ---------------- WALLET VIEWS ------------------------------


@api_view(['POST'])
def create_wallet(request):
    '''
    - ### **METHOD**: POST
    - ### **DESCRIPTION**: Create a new wallet with either email or phone number
    - ### **EXAMPLE**: {"email":"davykanye@gmail.com"}
    '''
    serializer = WalletSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_wallets(request):
    query = Wallet.objects.all()
    serializer = WalletSerializer(query, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_wallet(request, user):
    try:
        wallet = Wallet.search_object.find(user)
        serializer = WalletSerializer(wallet, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {
                'error': 'An error occurred',
                'exception': str(e)
            },
            exception=True
        )


@api_view(['DELETE'])
def delete_wallet(request, user):
    wallet = Wallet.search_object.find(user)

    wallet.delete()

    return Response('Wallet deleted successfully')
