import time

from aiogram.types import Message, WebAppInfo, MenuButtonWebApp

from loader import dp, bot, _


@dp.message_handler(commands="web_app")
async def _web_app_init(message: Message):
    web_app_uri = 'https://lite-task-bot-aiogram.vercel.app/NewReminder'
    web_app_uri += '?time=' + str(time.time())

    await bot.set_chat_menu_button(message.chat.id, MenuButtonWebApp(text='+New', web_app=WebAppInfo(url=web_app_uri)))

    text = _('Это более удобное и красивое меню для добавления напоминаний. Чтобы вызвать его, нажмите на кнопку "+New" рядом с полем ввода сообщений.\n\n'
             'P.S. Не рекомендуем использовать это меню в пк версии телеграма, так как там отображение пока-что некорректное. Надеемся что в скором времени Дуров все поправит.')

    await message.answer(text)

    await message.delete()
