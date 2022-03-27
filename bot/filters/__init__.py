from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters import Text

from loader import dp
from .admin import Admin
from .confirm_payment import ConfirmPayment
from .status import Status

if __name__ == 'bot.filters':
    dp.filters_factory.bind(ConfirmPayment)
    dp.filters_factory.bind(Admin)
    dp.filters_factory.bind(Status)
    dp.filters_factory.bind(Text)
    dp.filters_factory.bind(Regexp)
