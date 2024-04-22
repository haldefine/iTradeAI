from config import Stables
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
from binance.spot import Spot

spot_client = Spot()
exchange_info = spot_client.exchange_info()
volumes = spot_client.ticker_24hr()


def realVolume(base, quote):
    for i in volumes:
        if i['symbol'] == base + quote:
            if quote == 'USDT':
                return float(i['quoteVolume'])
            else:
                price = 0
                for j in volumes:
                    if j['symbol'] == quote + 'USDT':
                        price = float(j['lastPrice'])
                        break
                return float(i['quoteVolume']) * price


tracking_pairs = [f'{symbol["baseAsset"]}{symbol["quoteAsset"]}' for symbol in exchange_info["symbols"]
                  if symbol["quoteAsset"] in Stables and symbol["status"] == "TRADING" and symbol[
                      "isSpotTradingAllowed"] and realVolume(symbol["baseAsset"], symbol["quoteAsset"]) > 2500000]


# tracking_pairs = tracking_pairs[:100]

def log(msg1, msg2):
    print(msg1, msg2)

def run(message_handler):
    print('start', len(tracking_pairs))
    subscriptions = []
    for subsType in ['@kline_1s', '@ticker', '@avgPrice', '@depth20@1000ms']:
        for pair in tracking_pairs:
            subscriptions.append(f'{pair.replace("_", "").lower()}{subsType}')

    step = 150
    for i in range(0, len(subscriptions), step):
        streams_client = SpotWebsocketStreamClient(on_close=log, on_error=log, on_message=message_handler, is_combined=True)
        streams_client.send_message_to_server(subscriptions[i:i + step])
    print('binance started')