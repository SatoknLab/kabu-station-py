import urllib.request
import json

class Kabucom():
    def __init__(self, env: str = "development"):
        if env != "development" and env != "production":
            raise ValueError("env must be 'development' or 'production'") 

        self.env = env
        if env == "development":
            self.base_url = 'http://localhost:18081/kabusapi/'
        elif env == "production":
            self.base_url = 'http://localhost:18080/kabusapi/'

        self.token = None

    def authorize(self, password: str):
        param = {"APIPassword": password}
        response = self._send("POST", "token", param)

        self.token = response["Token"]

    def send_order(self,
                   order_password: str,
                   symbol: str,
                   exchange: str,
                   security_type: int,
                   side: int,
                   cash_margin: int,
                   deliv_type: int,
                   account_type: int,
                   qty: int,
                   front_order_type: int,
                   price: int,
                   expire_day: int,
                   margin_trade_type: int = None,
                   margin_premium_unit: float = None,
                   fund_type: int = None,
                   close_position_order: int = None,
                   close_positions: int = None,
                   reverse_limit_order: int = None) -> dict:
        if fund_type is not None:
            raise NotImplementedError("fund_type is not implemented yet")

        if close_position_order is not None:
            raise NotImplementedError("close_position_order is not implemented yet")
        
        if close_positions is not None:
            raise NotImplementedError("close_positions is not implemented yet")
        
        if reverse_limit_order is not None:
            raise NotImplementedError("reverse_limit_order is not implemented yet")
        
        if margin_trade_type is not None:
            raise NotImplementedError("margin_trade_type is not implemented yet")
        
        if margin_premium_unit is not None:
            raise NotImplementedError("margin_premium_unit is not implemented yet")
        
        required_param = {
            "Password": order_password,
            "Symbol": symbol,
            "Exchange": exchange,
            "SecurityType": security_type,
            "Side": side,
            "CashMargin": cash_margin,
            "DelivType": deliv_type,
            "AccountType": account_type,
            "Qty": qty,
            "FrontOrderType": front_order_type,
            "Price": price,
            "ExpireDay": expire_day
        }

        return self._send("POST", "sendorder", required_param)

    def cancel_order(self, order_id: str, order_password: str) -> dict:
        params = {"OrderId": order_id, "Password": order_password}
        return self._send("PUT", "cancelorder", params)

    def get_soft_limit(self) -> dict:
        return self._send("GET", "apisoftlimit", {})
    
    def get_wallet_cash(self) -> dict:
        return self._send("GET", "wallet/cash", {})

    def get_wallet_cash_by_symbol(self, symbol: str) -> dict:
        return self._send("GET", f"wallet/cash/{symbol}", {})

    def get_wallet_margin(self) -> dict:
        return self._send("GET", "wallet/margin", {})

    def get_wallet_margin_by_symbol(self, symbol: str) -> dict:
        return self._send("GET", f"wallet/margin/{symbol}", {})

    def get_wallet_future(self) -> dict:
        return self._send("GET", "wallet/future", {})

    def get_wallet_future_by_symbol(self, symbol: str) -> dict:
        return self._send("GET", f"wallet/future/{symbol}", {})

    def get_wallet_option(self) -> dict:
        return self._send("GET", "wallet/option", {})

    def get_wallet_option_by_symbol(self, symbol: str) -> dict:
        return self._send("GET", f"wallet/option/{symbol}", {})
    
    def get_board_by_symbol(self, symbol: str) -> dict:
        return self._send("GET", f"board/{symbol}", {})

    def get_symbol(self, symbol: str) -> dict:
        return self._send("GET", f"symbol/{symbol}", {})

    def get_orders(self,
                    product: int = None,
                    id: int = None,
                    updtime: int = None,
                    detail: bool = None,
                    symbol: str = None,
                    state: int = None,
                    side: int = None,
        ) -> dict :
        params = {}
        if product is not None:
            params["product"] = product
        if id is not None:
            params["id"] = id
        if updtime is not None:
            params["updtime"] = updtime
        if detail is not None:
            params["detail"] = detail
        if symbol is not None:
            params["symbol"] = symbol
        if state is not None:
            params["state"] = state
        if side is not None:
            params["side"] = side
        return self._send("GET", "orders", params)

    def get_positions(self) -> dict:
        return self._send("GET", "positions", {})

    def get_future_symbol_name(self) -> dict:
        raise NotImplementedError("get_future_symbol_name is not implemented yet")
    
    def get_option_symbol_name(self) -> dict:
        raise NotImplementedError("get_option_symbol_name is not implemented yet")

    def get_mini_option_weekly_symbol_name(self) -> dict:
        raise NotImplementedError("get_mini_option_weekly_symbol_name is not implemented yet")

    def get_ranking(self) -> dict:
        raise NotImplementedError("get_ranking is not implemented yet")
    
    def get_regulation_by_symbol(self, symbol: str) -> dict:
        return self._send("GET", f"regulation/{symbol}", {})

    def _send(self, method: str, path: str, data: dict) -> dict:
        req = self._make_request(method, path, data)

        with urllib.request.urlopen(req) as res:
            content = json.loads(res.read())
            return content

    def _make_request(self, method: str, path: str, data: dict) -> urllib.request.Request:
        url = self.base_url + path
        json_data = json.dumps(data).encode('utf8')
        req = urllib.request.Request(url, json_data, method=method)
        req.add_header('Content-Type', 'application/json')
        if self.token:
            req.add_header('X-API-KEY', self.token)
        return req
