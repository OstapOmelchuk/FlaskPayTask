import json

import flask
import jinja2
from flask import request, render_template, Blueprint, make_response

from product_payment_api.constants import shop_id, currency_list, payway
from product_payment_api.create_sign_hash import sign_formation
from product_payment_api.models.order_model import Order
import requests
import random

blp = Blueprint('post', __name__)


@blp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        res = int(request.form.get('user_currency'))
        if res == 978:
            return pay_by_euro()
        elif res == 840:
            return pay_by_usd()
        else:
            return pay_by_uah()
    else:
        return render_template('index.html')


def pay_by_euro():
    amount = request.form.get("amount")
    currency = request.form.get("user_currency")
    description = request.form.get("description")
    shop_order_id = random.randint(0, 10000000000)
    data_for_sign = {
        "amount": amount,
        "currency": currency,
        "shop_id": shop_id,
        "shop_order_id": shop_order_id,
    }
    sign = sign_formation(data_for_sign)
    order = Order.create(currency=currency, amount=amount, sign=sign, description=description)
    if not order:
        return make_response("Oops! Can not create an order", 400)
    data = {
        "amount": amount,
        "currency": currency,
        "shop_id": shop_id,
        "shop_order_id": shop_order_id,
        "description": description,
        "sign": sign
    }
    html_form = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>EUR Order</title>
    </head>
        <body>
            <form name="Pay" method="post" action="https://pay.piastrix.com/en/pay" accept-charset="UTF-8">
                <input type="hidden" name="amount" value={data['amount']} />
                <input type="hidden" name="currency" value={data['currency']} />
                <input type="hidden" name="shop_id" value={data['shop_id']} />
                <input type="hidden" name="sign" value='{data['sign']}' />
                <input type="hidden" name="shop_order_id" value={data['shop_order_id']} />
                <input type="hidden" name="description" value='{data['description']}' />
                <input type="submit" value="SUBMIT PAYMENT"/>
            </form>
        </body>
    </html>
    """

    tmplt = jinja2.Template(html_form)
    form = tmplt.render(data=data)

    return form


def pay_by_usd():
    shop_amount = request.form.get("amount")
    shop_currency = request.form.get("user_currency")
    description = request.form.get("description")
    shop_order_id = random.randint(0, 10000000000)
    payer_currency = random.sample(currency_list, 1)[0]

    data_for_sign = {
        "shop_amount": shop_amount,
        "shop_currency": shop_currency,
        "shop_id": shop_id,
        "shop_order_id": shop_order_id,
        "payer_currency": payer_currency
    }
    sign = sign_formation(data_for_sign)
    order = Order.create(currency=shop_currency, amount=shop_amount, sign=sign, description=description)
    if not order:
        return make_response("Oops! Can not create an order", 400)

    headers = {'Content-type': 'application/json'}
    data = {
        "shop_amount": shop_amount,
        "shop_currency": shop_currency,
        "shop_id": shop_id,
        "shop_order_id": shop_order_id,
        "description": description,
        "sign": sign,
        "payer_currency": payer_currency
    }
    r = requests.post('https://core.piastrix.com/bill/create', headers=headers, json=data)
    request_data = json.loads(r.text)

    print(request_data)

    if request_data["result"]:
        return flask.redirect(request_data['data']['url'])
    return make_response("Oops! Something wrong with Your request!", 400)


def pay_by_uah():
    amount = request.form.get("amount")
    currency = request.form.get("user_currency")
    description = request.form.get("description")
    shop_order_id = random.randint(0, 10000000000)

    data_for_sign = {
        "amount": amount,
        "currency": currency,
        "shop_id": shop_id,
        "shop_order_id": shop_order_id,
        "payway": payway
    }

    sign = sign_formation(data_for_sign)
    order = Order.create(currency=currency, amount=amount, sign=sign, description=description)
    if not order:
        return make_response("Oops! Can not create an order", 400)

    headers = {'Content-type': 'application/json'}
    data = {
        "amount": amount,
        "currency": currency,
        "shop_id": shop_id,
        "shop_order_id": shop_order_id,
        "sign": sign,
        "payway": payway,
        "description": description
    }
    r = requests.post('https://core.piastrix.com/invoice/create', headers=headers, json=data)

    return make_response("This method is disabled and no longer works. "
                         "(Message after post request: Payway (alias = advcash_rub) is not available for shop)")
