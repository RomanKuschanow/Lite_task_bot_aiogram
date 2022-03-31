import hashlib
import hmac
import json
from time import time
from uuid import uuid4

import requests
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from loader import config
from models import Bill, User
from utils.misc import save_execute, save_commit
from utils.misc.logging import logger


@save_execute
async def get_bill(session: AsyncSession, id: int) -> Bill:
    sql = select(Bill).where(Bill.id == id)
    query = await session.execute(sql)

    bill = query.scalar_one_or_none()

    return bill


@save_execute
async def get_bill_by_label(session: AsyncSession, label: str) -> Bill:
    sql = select(Bill).where(Bill.label == label).limit(1)
    query = await session.execute(sql)

    bill = query.scalar_one_or_none()

    return bill


@save_execute
async def update_bill_status(session: AsyncSession, bill: Bill, status: str) -> Bill:
    bill.status = status

    await save_commit(session)

    return bill


@save_execute
async def create_bill(session: AsyncSession, amount: int, user_id: int) -> Bill:
    new_bill = Bill(amount=amount, user_id=user_id, label=f'donate:{user_id}:{uuid4()}')

    session.add(new_bill)

    await save_commit(session)

    logger.info(f'New bill {new_bill}')

    return new_bill


def _generate_signature(merchant_key, data_str: str):
    return hmac.new(merchant_key.encode(), data_str.encode(), hashlib.md5).hexdigest()


def generate_invoice_link(bill: Bill, user: User) -> str:
    url = 'https://api.wayforpay.com/api'

    params = {
        'transactionType': 'CREATE_INVOICE',
        'merchantAccount': config.WAYFORPAY_ACCOUNT,
        'merchantAuthType': 'SimpleSignature',
        'merchantDomainName': 'http://t.me/Lite_task_bot',
        'apiVersion': 1,
        'language': user.language,
        'orderReference': bill.label,
        'orderDate': int(time()),
        'amount': bill.amount,
        'currency': 'USD',
        'orderTimeout': 86400,
        'productName': [
            f'Донат'
        ],
        'productPrice': [
            bill.amount
        ],
        'productCount': [
            1
        ]
    }
    data_str = ';'.join([
        params['merchantAccount'], params['merchantDomainName'], params['orderReference'],
        str(params['orderDate']), str(params['amount']), params['currency'], params['productName'][0],
        str(params['productCount'][0]), str(params['productPrice'][0])
    ])

    params['merchantSignature'] = _generate_signature(config.WAYFORPAY_SECRET, data_str)

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request('POST', url, headers=headers, data=json.dumps(params))

    link = response.json()['invoiceUrl']

    logger.info(f'Generate bill link: {link}')

    return link


@save_execute
async def check_bill(session: AsyncSession, bill: Bill, user: User) -> bool:
    url = 'https://api.wayforpay.com/api'

    params = {
        'transactionType': 'CHECK_STATUS',
        'merchantAccount': config.WAYFORPAY_ACCOUNT,
        'orderReference': bill.label,
        'apiVersion': 1
    }

    data_str = ';'.join([config.WAYFORPAY_ACCOUNT, bill.label])

    params['merchantSignature'] = _generate_signature(config.WAYFORPAY_SECRET, data_str)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', url, headers=headers, data=json.dumps(params))

    json_result = response.json()

    status = json_result['transactionStatus']
    amount = json_result['amount']

    if status != 'Approved':
        return False

    if bill.status == 'Approved':
        return True

    bill = await update_bill_status(session, bill, status)

    logger.info(f'Bill success {bill}, balance top up {amount}')

    return True
