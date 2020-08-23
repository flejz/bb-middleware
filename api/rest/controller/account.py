from flask import jsonify, request
from model.account import *

def init(app, account_handler):

    @app.route("/account/balance", methods=["GET", "POST"])
    def account_balances():
        if request.method == "GET":
            return account_handler.get_balances()
        elif request.method == "POST":
            address = get_address(request.json)
            amount = get_amount(request.json)
            account_handler.set_balance(address, amount)

    @app.route("/account/balance/<address>")
    def account_balance(address):
        return jsonify(account_handler.get_balance(address))

    @app.route("/account/median")
    def account_medians():
        return account_handler.get_medians()

    @app.route("/account/median/<address>")
    def account_median(address):
        return jsonify(account_handler.get_median(address))
