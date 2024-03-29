from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from services.bill import get_bill


class ConfirmPayment(BoundFilter):
    key = 'confirm_payment'

    def __init__(self, confirm_payment):
        self.confirm_payment = confirm_payment

    async def check(self, call: CallbackQuery):
        if isinstance(call, CallbackQuery):
            text = call.data
        else:
            return False

        if not text.startswith('confirm_payment_'):
            return False

        id = text[16:]
        if not id.isnumeric():
            return False

        bill = get_bill(int(id))

        if bill:
            return {'bill': bill}
