import requests, json
from datetime import datetime
class ZtoexController():
    ''' X-CH-SIGN = timestamp + method + requestPath + body
        X-CH-APIKEY = Your API-key
        X-CH-TS = Unix timestamp '''
        
    def __init__(self, api_key, api_secret, url="https://openapi.ztoex.com", api="/sapi/v1"):
        self.url = url
        self.api = api
        self.api_key = api_key
        self.api_secret = api_secret
        self.paths = {
            "ping": self.api + "/ping",
            "server_time": self.api + "/time",
            "list_pairs": self.api + "/symbols",
            "order_book": self.api + "/depth",
            "price_change": self.api + "/ticker",
            "trades": self.api + "/trades",
            "candlesticks": self.api + "/klines",
            "orders": self.api + "/order",
            "test_orders": self.api + "/order/test",
            "batch_orders": self.api + "/batchOrders",
            "balances": self.api + "/account"

        }

    
    def generate_sign(self, unix_time, method: str, url: str, data: str):
        import hmac
        import hashlib

        message = '{}{}{}{}'.format(unix_time, method.upper(), url, data)
        # message = '{}{}{}{}'.format("1588591856950", "POST", self.paths["test_orders"], "{\"symbol\":\"BTCUSDT\",\"price\":\"9300\",\"volume\":\"1\",\"side\":\"BUY\",\"type\":\"LIMIT\"}")
        return hmac.new(bytes(self.api_secret , 'latin-1'), msg = bytes(message , 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()

        
        

    def send_request(self, method, url, headers=None, data=None):
            """ Handles sending requests """
            unix_time = datetime.utcnow().timestamp()
            x_ch_sign = self.generate_sign(unix_time, method, url, data)
            url = self.url + url
            print(unix_time)
            
            headers = {
                'X-CH-APIKEY': self.api_key,
                'X-CH-TS': str((unix_time + 3600) * 1000).split(".")[0],
                'Content-Type': 'application/json',
                'X-CH-SIGN': x_ch_sign
                }

            try:
                if "get" in method.lower():
                    response = requests.get(url=url, headers=headers, verify=False)
                elif "post" in method.lower():
                    response = requests.post(
                        url=url, headers=headers, json=data, verify=False
                    )
                elif "put" in method.lower():
                    response = requests.put(
                        url=url, headers=headers, json=data, verify=False
                    )
                elif "delete" in method.lower():
                    response = requests.delete(url=url, headers=headers, verify=False)
                response.raise_for_status()

            except requests.exceptions.ConnectionError as connection_error:
                print("Error Connecting:", connection_error)
                sys.exit(1)
            except requests.exceptions.Timeout as timeout_error:
                print("Timeout Error:", timeout_error)
                sys.exit(1)
            except requests.exceptions.RequestException as err:
                print("Error:", err)

            content = None
            try:
                content = json.loads(response.content.decode("utf8"))
            except json.JSONDecodeError:
                content = response.content.decode("utf8")

            if int(response.status_code) >= 200 and int(response.status_code) <= 399:
                print(f"URL: [{url}]\nResponse code: [{response.status_code}]")
                if not content:
                    print("Response was null")
                else:
                    return content
            else:
                print(
                    f"Error sending requests [{response.status_code}] with error message [{content}]\nRequest:\nurl:{str(url)}"
                )
