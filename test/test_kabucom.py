from src.kabucom import Kabucom
from src.enums.exchange import Exchange
from src.enums.security_type import SecurityType
from src.enums.side import Side
from src.enums.cash_margin import CashMargin
from src.enums.margin_trade_type import MarginTradeType
from src.enums.deliv_type import DelivType
from src.enums.account_type import AccountType
from src.enums.front_order_type import FrontOrderType


class TestKabucom():
    def test_init_development(self):
        kabucom = Kabucom()
        assert kabucom.env == "development"
        assert kabucom.base_url == "http://localhost:18081/kabusapi/"
        assert kabucom.token == None


    def test_init_production(self):
        kabucom = Kabucom("production")
        assert kabucom.env == "production"
        assert kabucom.base_url == "http://localhost:18080/kabusapi/"
        assert kabucom.token == None


    def test_init_invalid(self):
        try:
            kabucom = Kabucom("invalid")
        except ValueError as e:
            assert str(e) == "env must be 'development' or 'production'"


    def test_authorize(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "Token": "token"})
        kabucom.authorize("password")
        assert kabucom.token == "token"


    def test_get_soft_limit(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "Current": 100, "Max": 1000})
        assert kabucom.get_soft_limit() == {"ResultCode": 0, "Current": 100, "Max": 1000}


    def test_get_wallet_cash(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "StockAccountWallet": 1000000, "MarginAccountWallet": 1000000})
        assert kabucom.get_wallet_cash() == {"ResultCode": 0, "StockAccountWallet": 1000000, "MarginAccountWallet": 1000000}


    def test_send_order(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "OrderId": "order_id"})

        order_password = "password"
        symbol = "9433"
        exchange = Exchange.TOUSHOU
        security_type = SecurityType.STOCK
        side = Side.BUY
        cash_margin = CashMargin.CASH
        deliv_type = DelivType.DEPOSIT
        account_type = AccountType.SPECIAL
        qty = 500
        front_order_type = FrontOrderType.LIMIT
        expire_day = 20240101

        assert kabucom.send_order(order_password=order_password,
                                    symbol=symbol,
                                    exchange=exchange,
                                    security_type=security_type,
                                    side=side,
                                    cash_margin=cash_margin,
                                    margin_trade_type=None,
                                    deliv_type=deliv_type,
                                    account_type=account_type,
                                    qty=qty,
                                    price=1000,
                                    front_order_type=front_order_type,
                                    expire_day=expire_day) == {"ResultCode": 0, "OrderId": "order_id"}

    def test_cancel_order(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "OrderId": "order_id"})

        order_id = "order_id"
        order_password = "password"
        assert kabucom.cancel_order(order_id, order_password) == {"ResultCode": 0, "OrderId": "order_id"}

    def test_get_wallet_cash_by_symbol(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "Symbol": "9433", "Current": 1000000, "Incoming": 1000000, "Outgoing": 1000000})
        assert kabucom.get_wallet_cash_by_symbol("9433") == {"ResultCode": 0, "Symbol": "9433", "Current": 1000000, "Incoming": 1000000, "Outgoing": 1000000}

    def test_get_wallet_margin(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "StockAccountWallet": 1000000, "MarginAccountWallet": 1000000})
        assert kabucom.get_wallet_margin() == {"ResultCode": 0, "StockAccountWallet": 1000000, "MarginAccountWallet": 1000000}

    def test_get_wallet_margin_by_symbol(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "Symbol": "9433", "Current": 1000000, "Incoming": 1000000, "Outgoing": 1000000})
        assert kabucom.get_wallet_margin_by_symbol("9433") == {"ResultCode": 0, "Symbol": "9433", "Current": 1000000, "Incoming": 1000000, "Outgoing": 1000000}

    def test_get_wallet_future(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "StockAccountWallet": 1000000, "MarginAccountWallet": 1000000})
        assert kabucom.get_wallet_future() == {"ResultCode": 0, "StockAccountWallet": 1000000, "MarginAccountWallet": 1000000}

    def test_get_wallet_future_by_symbol(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "Symbol": "9433", "Current": 1000000, "Incoming": 1000000, "Outgoing": 1000000})
        assert kabucom.get_wallet_future_by_symbol("9433") == {"ResultCode": 0, "Symbol": "9433", "Current": 1000000, "Incoming": 1000000, "Outgoing": 1000000}

    def test_get_wallet_option(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "StockAccountWallet": 1000000, "MarginAccountWallet": 1000000})
        assert kabucom.get_wallet_option() == {"ResultCode": 0, "StockAccountWallet": 1000000, "MarginAccountWallet": 1000000}

    def test_get_wallet_option_by_symbol(self, mocker):
        kabucom = Kabucom()
        mocker.patch.object(kabucom, "_send", return_value={"ResultCode": 0, "Symbol": "9433", "Current": 1000000, "Incoming": 1000000, "Outgoing": 1000000})
        assert kabucom.get_wallet_option_by_symbol("9433") == {"ResultCode": 0, "Symbol": "9433", "Current": 1000000, "Incoming": 1000000, "Outgoing": 1000000}

    def test_get_board_by_symbol(self, mocker):
        kabucom = Kabucom()
        expected_result = {
            "expetcted": "result"
        }

        mocker.patch.object(kabucom, "_send", return_value=expected_result)
        assert kabucom.get_board_by_symbol("9433") == expected_result

    def test_get_symbol(self, mocker):
        kabucom = Kabucom()
        expected_result = {
            "expetcted": "result"
        }

        mocker.patch.object(kabucom, "_send", return_value=expected_result)
        assert kabucom.get_symbol("9433") == expected_result

    def test_get_orders(self, mocker):
        kabucom = Kabucom()
        expected_result = {
            "expetcted": "result"
        }

        mocker.patch.object(kabucom, "_send", return_value=expected_result)
        assert kabucom.get_orders() == expected_result
        assert kabucom.get_orders(product=1) == expected_result
        assert kabucom.get_orders(id=1) == expected_result
        assert kabucom.get_orders(updtime=1) == expected_result
        assert kabucom.get_orders(detail=True) == expected_result
        assert kabucom.get_orders(symbol="9433") == expected_result
        assert kabucom.get_orders(state=1) == expected_result
        assert kabucom.get_orders(side=1) == expected_result
        assert kabucom.get_orders(product=1, id=1, updtime=1, detail=True, symbol="9433", state=1, side=1) == expected_result

    def test_get_positions(self, mocker):
        kabucom = Kabucom()
        expected_result = {
            "expetcted": "result"
        }

        mocker.patch.object(kabucom, "_send", return_value=expected_result)
        assert kabucom.get_positions() == expected_result

    def test_get_regulation_by_symbol(self, mocker):
        kabucom = Kabucom()
        expected_result = {
            "expetcted": "result"
        }

        mocker.patch.object(kabucom, "_send", return_value=expected_result)
        assert kabucom.get_regulation_by_symbol("9433") == expected_result
