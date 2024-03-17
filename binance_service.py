from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
# from config import tracking_pairs
import time
from binance.spot import Spot

spot_client = Spot()
exchange_info = spot_client.exchange_info()
# print(exchange_info["symbols"][0])
tracking_pairs = [f'{symbol["baseAsset"]}{symbol["quoteAsset"]}' for symbol in exchange_info["symbols"]
                  if symbol["quoteAsset"] == "USDT" and symbol["status"] == "TRADING" and symbol["isSpotTradingAllowed"]]


def run(message_handler):
    print('start', len(tracking_pairs))
    subscriptions = []
    for subsType in ['@kline_1s', '@ticker', '@avgPrice', '@depth20@1000ms']:
        for pair in tracking_pairs:
            subscriptions.append(f'{pair.replace("_", "").lower()}{subsType}')

    step = 150
    for i in range(0, len(subscriptions), step):
        streams_client = SpotWebsocketStreamClient(on_message=message_handler, is_combined=True)
        streams_client.send_message_to_server(subscriptions[i:i+step])




