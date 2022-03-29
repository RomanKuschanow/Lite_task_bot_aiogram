from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot.keyboards.inline.payment import get_payment_inline_markup
from bot.states import Donate
from loader import dp, _
from models import User, Bill
from services.bill import create_bill, generate_invoice_link, check_bill
from services.user import update_status
from utils.misc.logging import logger


@dp.message_handler(commands='donate', state='*')
async def _user_top_up_balance(message: Message):
    text = _('Напиши сумму в долларах (минимум 1), которую хотите задонатить')

    await message.answer(text)
    await Donate.top_up_balance.set()


@dp.message_handler(state=Donate.top_up_balance)
async def _user_top_up_balance_invoice(message: Message, user: User, session, state):
    amount = message.text
    if not amount.isnumeric() or int(message.text) < 1:
        return await message.answer(_('Введите целое число больше 0, например: 5'))

    bill = await create_bill(session, amount, message.from_user.id)
    logger.info(f'{user} create {bill}')

    link = generate_invoice_link(bill, user)

    text = _('Номер: {id}\n'
             'Донат на сумму: {amount}$\n\n' +
             ('После оплаты нажмите "Оплатил ✅", и получите полный доступ к функционалу бота'
              if not user.is_vip else '')).format(id=bill.id, amount=amount)

    await message.answer(text, reply_markup=get_payment_inline_markup(link, bill.id if not user.is_vip else None))
    await state.finish()


@dp.callback_query_handler(state='*', confirm_payment=True)
async def _check_bill(callback_query: CallbackQuery, bill: Bill, session, user: User):
    bill = await check_bill(session, bill, user)

    if bill:
        await callback_query.message.delete()
        await update_status(session, user.id, True)
        return await callback_query.message.answer(_('Оплата прошла успешно ✅'))

    return await callback_query.answer(_('Оплата еще не прошла, нажмите на кнопку чуть позже'), show_alert=True)
