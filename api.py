import logging

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiohttp import web
from aiohttp.web_request import Request

from loader import bot, _, config
from models.base import create_async_database
from services.bill import get_bill_by_label, check_bill
from services.user import get_user, update_status
from utils import generate_inline_id
from utils.web_app import check_webapp_signature, parse_webapp_init_data
from aiohttp_middlewares import cors_middleware


routes = web.RouteTableDef()
logging.basicConfig(level=logging.INFO)
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 3313


@routes.post('/wayforpay/uidhfghuir9u3i82oguisho09238uryosdh')
async def _wayforpay(request: Request):
    session = await create_async_database()

    data = await request.json()

    label = data['orderReference']

    logging.info(label)

    bill = await get_bill_by_label(session, label)
    if bill:
        if not bill or not await check_bill(session, bill):
            await session.close()
            return web.json_response({'ok': True})

        user = await get_user(session, bill.user_id)
        if user.is_vip:
            await bot.send_message(bill.user_id, _('Оплата прошла успешно ✅'))
        else:
            await update_status(session, bill.user_id, True)

    await session.close()

    return web.json_response({'ok': True})


@routes.post('/api/getStatus')
async def _api_get_status(request: Request):
    data = await request.json()

    if '_auth' not in data or not check_webapp_signature(config.BOT_TOKEN, data['_auth']):
        return web.json_response({'ok': False, 'message': 'invalid signature'}, status=401)

    telegram_data = parse_webapp_init_data(data['_auth'])
    session = await create_async_database()

    user = await get_user(session, int(telegram_data['user']['id']))

    return web.json_response({'ok': True, 'isVip': user.is_vip or user.is_admin})


@routes.post('/api/NewReminder')
async def _api_new_reminder(request: Request):
    data = await request.json()
    if '_auth' not in data or not check_webapp_signature(config.BOT_TOKEN, data['_auth']):
        return web.json_response({'ok': False, 'message': 'invalid signature'}, status=401)

    telegram_data = parse_webapp_init_data(data['_auth'])

    logging.info(telegram_data)
    logging.info(telegram_data['user']['id'])

    await bot.send_message(telegram_data['user']['id'], f'WebAppInitData:\n<pre>{telegram_data}</pre>\n\n'
                                                        f'Data:\n<pre>{data["data"]}</pre>')
    try:
        inline_query = telegram_data['query_id']
        item = InlineQueryResultArticle(id=generate_inline_id(inline_query), title='Test',
                                        input_message_content=InputTextMessageContent('Some answer'))
        await bot.answer_web_app_query(inline_query, item)
    except:
        pass

    return web.json_response({'ok': True})


app = web.Application(middlewares=[cors_middleware(allow_all=True)])
app.add_routes(routes)
web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)