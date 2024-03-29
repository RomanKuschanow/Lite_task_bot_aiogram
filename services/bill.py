import hashlib
import hmac
import json
from time import time
from uuid import uuid4

import requests

from loader import config
from models import Bill, User
from utils.misc.logging import logger


def get_bill(id: int) -> Bill:
    return Bill.get_or_none(Bill.id == id)


def get_bill_by_label(label: str) -> Bill:
    return Bill.get_or_none(Bill.label == label)


def update_bill_status(bill: Bill, status: str) -> Bill:
    bill.status = status
    bill.save()

    return bill


def create_bill(amount: int, user_id: int) -> Bill:
    new_bill = Bill.create(amount=amount, user_id=user_id, label=f'donate:{user_id}:{uuid4()}')

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


def check_bill(bill: Bill) -> bool:
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

    bill = update_bill_status(bill, status)

    logger.info(f'Bill success {bill}, balance top up {amount}')

    return True
