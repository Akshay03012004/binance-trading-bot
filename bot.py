import os
import time
import hmac
import hashlib
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("trading_bot.log"), logging.StreamHandler()]
)

BASE_URL = "https://testnet.binancefuture.com"

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {"X-MBX-APIKEY": self.api_key}

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        endpoint = "/fapi/v1/order"
        timestamp = int(time.time() * 1000)
        params = {"symbol": symbol.upper(), "side": side.upper(), "type": order_type.upper(), "quantity": quantity, "timestamp": timestamp}
        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = self._generate_signature(query_string)
        url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
        try:
            response = requests.post(url, headers=self.headers)
            data = response.json()
            if response.status_code == 200:
                logging.info(f"Order SUCCESS! OrderID: {data.get('orderId')}")
                return data
            else:
                logging.error(f"Order FAILURE: {data.get('msg')}")
        except Exception as e:
            logging.error(f"Failure: {str(e)}")