from loader import dp
from .admin import Admin
from.status import Status
from aiogram.dispatcher.filters import Text

if __name__ == 'filters':
    dp.filters_factory.bind(Admin)
    dp.filters_factory.bind(Status)
    dp.filters_factory.bind(Text)
