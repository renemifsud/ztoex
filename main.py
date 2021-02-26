import requests, json, time
from ztoex_controller import ZtoexController



def main():
    url = "https://openapi.ztoex.com/sapi/v1/ticker?symbol=dpb1373usdt"
    # payload = "{\"symbol\":\"BTCUSDT\",\"volume\":1,\"side\":\"BUY\",\"type\":\"LIMIT\",\"price\":10000,\"newClientOrderId\":\"\",\"recvWindow\":5000}"

    try:
        response = requests.request("GET", url)
        print(response.json()["last"])
    except:
        print("failed getting data")




if __name__ == "__main__":
    ztoex = ZtoexController()
    json.loads(ztoex.send_request("GET", ztoex.paths["server_time"]))["serverTime"]
    # while(True):
    #     main()
    #     time.sleep(0.5)