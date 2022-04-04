from aiogram.types import Message

from bot.keyboards.default.menu import get_menu_keyboard_markup
from loader import dp, _


@dp.message_handler(commands='help')
async def help(message: Message, user):
    text = _('/start — Запуск бота\n'
             '/help — Вывод этого списка\n'
             '/new_reminder — Создать новое напоминание. Необходимо ввести название, выбрать дату '
             'и точное время напоминания\n'
             '/reminders_list — Отобразит список всех напоминаний. С помощью клавиатуры под сообщением '
             'можно будет отфильтровать их для более удобного поиска, а так же изменить название и/или время\n'
             '/donate — Пожертвовать разработчикам (минимум 1 доллар)\n'
             '/feedback — Обратная связь с разработчиками\n'
             '/menu — Отобразит меню если оно по какой-то причине пропало\n'
             '/lang — Позволяет сменить язык\n'
             '/tz — Выбрать часовой пояс\n'
             '/reset — Сбрасывает состояние бота. Полезно если при создании или редактировании'
             ' напоминания бот стал вести себя не корректно\n\n') + \
           ("" if user.is_admin else (_('‼ Если ты еще не донатил, тебе не доступны или ограничены некоторые функции:\n'
                                        '❌ Фильтры\n'
                                        '❌ Редактирование (в меню редактирования доступна только кнопка удаления)\n'
                                        '❌ Одновременно можно создать только 5 активных напоминаний') if not user.is_vip else ""))

    await message.answer(text, reply_markup=get_menu_keyboard_markup())
    await message.delete()
