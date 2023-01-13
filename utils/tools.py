from utils.banks import bank_list
from slugify import slugify


def get_bank_code(name):
    banks = bank_list()
    slug = slugify(name)
    output = None
    for bank in banks:
        if bank['slug'] == slug:
            output = bank
            break
        else:
            pass

    return output.get('code')


def check_wallet(wallet, amount):
    if amount > wallet:
        raise Exception("Insufficient amount in wallet")
