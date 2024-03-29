from datetime import datetime, date
import pytz

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton
from aiogram_datepicker import DatepickerSettings, DatepickerCustomAction

from loader import _


def _get_datepicker_settings(tz: str, hidden_back: bool = False, hidden_cancel: bool = False):
    state_panel = []
    server_date = pytz.timezone("UTC").localize(datetime.now())

    if not hidden_back:
        state_panel.append('back')
    if not hidden_cancel:
        state_panel.append('cancel')

    class TodayAction(DatepickerCustomAction):
        action: str = 'today'
        label: str = _('Сегодня')

        available_views = ('day',)

        def get_action(self, view: str, year: int, month: int, day: int) -> InlineKeyboardButton:
            return InlineKeyboardButton(self.label,
                                        callback_data=self._get_callback(view, self.action, year, month, day))

        async def process(self, query: CallbackQuery, view: str, _date: date) -> bool:
            if view == 'day':
                await self.set_view(query, 'day', datetime.now().date())
                return False
            elif view == 'month':
                await self.set_view(query, 'month', date(_date.year, datetime.now().date().month, _date.day))
                return False
            elif view == 'year':
                await self.set_view(query, 'month', date(datetime.now().date().year, _date.month, _date.day))
                return False

    class CancelAction(DatepickerCustomAction):
        action: str = 'cancel'
        label: str = _('❌ Отмена')

        available_views = ('day', 'month', 'year')

        def get_action(self, view: str, year: int, month: int, day: int) -> InlineKeyboardButton:
            return InlineKeyboardButton(self.label, callback_data='cancel')

        async def process(self, query: CallbackQuery, view: str, _date: date) -> bool:
            return False

    class BackAction(DatepickerCustomAction):
        action: str = 'back'
        label: str = _('⬅ Назад')

        available_views = ('day', 'month', 'year')

        def get_action(self, view: str, year: int, month: int, day: int) -> InlineKeyboardButton:
            return InlineKeyboardButton(self.label, callback_data='back')

        async def process(self, query: CallbackQuery, view: str, _date: date) -> bool:
            return False

    return DatepickerSettings(
        initial_view='day',  # available views -> day, month, year
        initial_date=server_date.astimezone(pytz.timezone(tz)).date(),  # default date
        views={
            'day': {
                'show_weekdays': True,
                'weekdays_labels': ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
                'header': ['prev-year', 'days-title', 'next-year'],
                'footer': ['prev-month', 'today', 'next-month',
                           state_panel],
                # available actions -> prev-year, days-title, next-year, prev-month, select, next-month, ignore
            },
            'month': {
                'show_weekdays': True,
                'months_labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                'header': ['prev-year', 'year', 'next-year'],
                'footer': ['today',
                           state_panel],
                # available actions -> prev-year, year, next-year, select, ignore
            },
            'year': {
                'show_weekdays': True,
                'header': ['prev-years', 'next-years'],
                'footer': ['today',
                           state_panel],
                # available actions -> prev-years, ignore, next-years
            }
        },
        labels={
            'prev-year': '<<',
            'next-year': '>>',
            'prev-years': '<<',
            'next-years': '>>',
            'days-title': '{month} {year}',
            'selected-day': '{day} *',
            'selected-month': '{month} *',
            'present-day': '• {day} •',
            'prev-month': '<',
            'select': _('Выбрать'),
            'next-month': '>',
            'ignore': ''
        },
        custom_actions=[TodayAction, CancelAction, BackAction]  # some custom actions
    )
