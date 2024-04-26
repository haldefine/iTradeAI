import json
import time

import h5py
import numpy as np

import binance_service
import config
from web import runServer


def showData(pair):
    with h5py.File('datasets/data.h5', 'r') as file:
        if pair in file:
            pair_dataset = file[pair]

            print(pair_dataset[-1])
        else:
            print(f"No data for pair {pair}")


def processData(subsType, data):
    if subsType == 'kline_1s':
        return [int(data['k']['T']), float(data['k']['o']), float(data['k']['h']), float(data['k']['l']),
                float(data['k']['c']),
                float(data['k']['v']), float(data['k']['q']), float(data['k']['V']), float(data['k']['Q']),
                int(data['k']['n'])]
    elif subsType == 'ticker':
        return [float(data['P']), float(data['p']), float(data['w']), float(data['x']), float(data['c']),
                float(data['Q']), float(data['b']), float(data['B']), float(data['a']), float(data['A']),
                float(data['o']), float(data['h']), float(data['l']), float(data['v']), float(data['q']),
                int(data['n'])]
    elif subsType == 'avgPrice':
        return [float(data['w'])]
    elif subsType == 'depth20':
        return [[float(bid[0]), float(bid[1])] for bid in data['bids']] + [[float(ask[0]), float(ask[1])] for ask in
                                                                           data['asks']]


def writeData():
    with h5py.File(config.file_path, 'a') as file:
        for pair in Data:

            is_full = True
            for type in SubTypes:
                if type not in Data[pair]:
                    is_full = False
                    break
            if not is_full:
                continue

            row_data = np.concatenate([Data[pair][type] for type in SubTypes])

            if pair not in file:
                pair_dataset = file.create_dataset(pair, shape=(0, row_data.shape[0]), maxshape=(None, row_data.shape[0]),
                                                   compression='gzip', compression_opts=9)
            else:
                pair_dataset = file[pair]

            pair_dataset.resize((pair_dataset.shape[0] + 1, pair_dataset.shape[1]))

            pair_dataset[-1] = row_data




SubTypes = ['kline_1s', 'ticker', 'avgPrice', 'depth20']
Data = {}
LastTimestampWritten = 0


def message_handler(_, message):
    global Data
    global LastTimestampWritten

    message = json.loads(message)
    if 'stream' not in message:
        print(message)
        return
    subsType = message['stream'].split('@')[1]
    pair = message['stream'].split('@')[0]
    processed_data = processData(subsType, message['data'])
    new_data = np.array(processed_data).flatten()

    if subsType == 'kline_1s':
        if new_data[0] > LastTimestampWritten:
            LastTimestampWritten = new_data[0]
            writeData()

    if pair not in Data:
        Data[pair] = {}
    Data[pair][subsType] = new_data


if __name__ == '__main__':
    binance_service.run(message_handler)
    runServer()
