from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from bot.keyboards.inline.payment import get_payment_inline_markup
from bot.keyboards.default.menu import get_menu_keyboard_markup
from bot.states import Donate
from loader import dp, _, bot
from models import User, Bill
from services.bill import create_bill, generate_invoice_link, check_bill
from services.user import update_status
from utils.misc.logging import logger


@dp.message_handler(commands='donate', state='*')
async def donate(message: Message, state):
    bot_message = await message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, bot_message.message_id)

    text = _('Напиши сумму в долларах (минимум 1), которую хотите задонатить')

    bot_message = await message.answer(text)
    await Donate.top_up_balance.set()

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=Donate.top_up_balance, menu=False)
async def donate_invoice(message: Message, user: User, session, state):
    amount = message.text
    if not amount.isnumeric() or int(message.text) < 1:
        bot_message = await message.answer(_('Введите целое число больше 0, например: 5'))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    bill = await create_bill(session, amount, message.from_user.id)
    logger.info(f'{user} create {bill}')

    link = generate_invoice_link(bill, user)

    await message.answer(_("Спасибо. Следующее сообщение это чек. Если возникнут проблемы или вопросы по поводу оплаты, "
                           "укажи в сообщении номер чека"), reply_markup=get_menu_keyboard_markup(user.is_admin))

    text = _('Номер: {id}\n'
             'Донат на сумму: {amount}$\n\n').format(id=bill.id, amount=amount)

    await message.answer(text, reply_markup=get_payment_inline_markup(link))

    async with state.proxy() as data:
        data['message'].append(message.message_id)

        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await state.finish()
