import logging
from datetime import datetime

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_middlewares import cors_middleware

from loader import bot, _, config
from services.bill import get_bill_by_label, check_bill
from services.reminder import create_reminder, edit_freely, get_all_actual_by_user_id
from services.user import get_user, update_status
from utils.web_app import check_webapp_signature, parse_webapp_init_data

routes = web.RouteTableDef()
logging.basicConfig(level=logging.INFO)
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 3313


@routes.post('/wayforpay/uidhfghuir9u3i82oguisho09238uryosdh')
async def _wayforpay(request: Request):
    data = await request.json()

    label = data['orderReference']

    logging.info(label)

    bill = get_bill_by_label(label)
    if bill:
        if not bill or not check_bill(bill):
            return web.json_response({'ok': True})

        user = get_user(bill.user_id)
        if user.is_vip:
            await bot.send_message(bill.user_id, _('Оплата прошла успешно ✅'))
        else:
            update_status(bill.user_id, True)

    return web.json_response({'ok': True})
    

@routes.post('/api/getUser')
async def _api_get_status(request: Request):
    data = await request.json()

    if '_auth' not in data or not check_webapp_signature(config.BOT_TOKEN, data['_auth']):
        return web.json_response({'ok': False, 'message': 'invalid signature'}, status=401)

    telegram_data = parse_webapp_init_data(data['_auth'])

    user = get_user(int(telegram_data['user']['id']))

    return web.json_response({'isVip': user.is_vip or user.is_admin, 'lang': user.language})


@routes.post('/api/NewReminder')
async def _api_new_reminder(request: Request):
    data = await request.json()
    if '_auth' not in data or not check_webapp_signature(config.BOT_TOKEN, data['_auth']):
        return web.json_response({'ok': False, 'message': 'invalid signature'}, status=401)

    telegram_data = parse_webapp_init_data(data['_auth'])

    logging.info(telegram_data)
    logging.info(telegram_data['user']['id'])
    logging.info(data['data'])

    user = get_user(int(telegram_data['user']['id']))

    text = _(
        'К сожалению разработчикам тоже нужно что-то кушать, по этому некоторые функции доступны только после '
        'доната. Это можно сделать введя команду /donate, а так же воспользовавшись реферальной ссылкой /referral')

    if not (user.is_vip or user.is_admin):
        reminders = get_all_actual_by_user_id(user.id)
        if len(reminders) >= 5:
            await bot.send_message(telegram_data['user']['id'], text)
            return web.json_response({'ok': True})

    reminder = create_reminder(telegram_data['user']['id'], data['data']['text'],
                               datetime.strptime(data['data']['date'], '%Y-%m-%dT%H:%M:%S.%fZ'), False)
    if data['data']['repeat']:
        if data['data']['type'] == 'count':
            reminder = edit_freely(reminder.id, reminder.user_id, is_repeat=True,
                                   repeat_count=(-1 if data['data']['inf'] else int(data['data']['count'])),
                                   repeat_range=data['data']['range'], repeat_until=None)
        else:
            reminder = edit_freely(reminder.id, reminder.user_id, is_repeat=True,
                                   repeat_until=datetime.strptime(data['data']['untilDate'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                   repeat_range=data['data']['range'], repeat_count=None)

    from utils import get_text
    await bot.send_message(telegram_data['user']['id'], get_text(reminder))

    return web.json_response({'ok': True})


app = web.Application(middlewares=[cors_middleware(allow_all=True)])
app.add_routes(routes)
web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
