# from config import Base
from utils.config import Base
from utils.tools import get_bank_code


class Transfer(Base):
    def __init__(self, reason):
        super().__init__()
        self.reason = reason
        self.source = 'balance'
        self.recipient = ''

    def _create_recipient(self, data):
        bank_code = get_bank_code(data.get('bank_name'))  #
        payload = {
            'type': 'nuban',
            'name': 'Default recipient',
            'account_number': data.get('account_number'),
            'bank_code': bank_code,
            'currency': 'NGN'
        }
        response = self._request('transferrecipient', 'POST', payload)
        print(response)
        return response

    def _set_recipient(self, recipient):
        self.recipient = recipient

    def _transfer(self, amount):
        payload = {
            'source': self.source,
            'reason': self.reason,
            'amount': amount,
            'recipient': self.recipient
        }

        response = self._request('transfer', 'POST', payload)
        print(response)
        return response


class TransferControl(Base):
    """docstring for Transfer Control."""

    def _disable_otp(self, payload):
        pass

    def _confirm_disable_otp(self, payload):
        pass
