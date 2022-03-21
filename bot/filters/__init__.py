from loader import dp
from .admin import Admin
from.status import Status
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters import Regexp

if __name__ == 'filters':
    dp.filters_factory.bind(Admin)
    dp.filters_factory.bind(Status)
    dp.filters_factory.bind(Text)
    dp.filters_factory.bind(Regexp)
