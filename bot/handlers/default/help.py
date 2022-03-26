from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from loader import dp, _


@dp.message_handler(commands='help')
async def help(message: Message):
    text = _("/start — Запуск бота\n"
             "/help — Вывод этого списка\n"
             "/new_reminder — Создать новое напоминание. Необходимо ввести название, выбрать дату и точное время напоминания\n"
             "/reminders_list — Отобразит список всех напоминаний. С помощью клавиатуры под сообщением можно будет отфильтровать их для более удобного поиска, а так же изменить название и/или время\n"
             "/feedback — Обратная связь с разработчиками\n"
             "/lang — Позволяет сменить язык\n"
             "/reset — Сбрасывает состояние бота. Полезно если при создании или редактировании напоминания бот стал вести себя не корректно")

    await message.answer(text)

    await message.delete()

