import logging

from aiohttp import web
from aiohttp.web_request import Request

from loader import bot, _
from models.base import create_async_database
from services.bill import get_bill_by_label, check_bill
from services.user import get_user, update_status

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


app = web.Application()
app.add_routes(routes)
web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
