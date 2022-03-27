from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot.keyboards.inline.payment import get_payment_inline_markup
from bot.states import Balance
from loader import dp
from models import User, Bill
from services.bill import create_bill, generate_invoice_link, check_bill
from utils.misc.logging import logger


@dp.message_handler(commands='balance', state='*')
async def _user_balance(message: Message, user: User):
    text = f'Баланс: {round(user.balance, 2)} грн.'

    await message.answer(text)


@dp.message_handler(commands='donate', state='*')
async def _user_top_up_balance(message: Message, user: User):
    text = (f'Текущий баланс: {round(user.balance, 2)} грн.\n\n'
            f'Выбери ниже или напиши сумму в грнлях, на которую хотите пополнить баланс 👇')

    await message.answer(text)
    await Balance.top_up_balance.set()


@dp.message_handler(state=Balance.top_up_balance)
async def _user_top_up_balance_invoice(message: Message, user: User, session, state):
    amount = message.text
    if not amount.isnumeric():
        return await message.answer('Введите целое число, например: 550')

    bill = await create_bill(session, amount, message.from_user.id)
    logger.info(f'{user} create {bill}')

    link = generate_invoice_link(bill)

    text = (f'Номер: {bill.id}\n'
            f'Пополнение баланса на сумму: {amount}\n\n'
            f'После оплаты нажмите на кнопку "Оплатил ✅"')

    await message.answer(text, reply_markup=get_payment_inline_markup(link, bill.id))
    await state.finish()


@dp.callback_query_handler(state='*', confirm_payment=True)
async def _check_bill(call: CallbackQuery, bill: Bill, session, user: User):
    bill = await check_bill(session, bill, user)

    if bill:
        await call.message.delete()
        return await call.message.answer('Оплата прошла успешно ✅')

    return await call.answer('Оплата еще не прошла, нажмите на кнопку чуть позже', show_alert=True)
