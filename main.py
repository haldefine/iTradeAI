import json

import numpy as np

import binance_service
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Trading Bot")
root.geometry("1280x720")

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

text_field1 = ttk.Entry(frame)
text_field1.pack(fill=tk.X, pady=5)

text_field2 = ttk.Entry(frame)
text_field2.pack(fill=tk.X, pady=5)

text_field3 = ttk.Entry(frame)
text_field3.pack(fill=tk.X, pady=5)

output_label = ttk.Label(frame, wraplength=300)
output_label.pack(pady=10)


def on_button_click():
    binance_service.run(display_message)


submit_button = ttk.Button(frame, text="Submit", command=on_button_click)
submit_button.pack(pady=10)

data = {
    'kline_1s': {},
    'ticker': {},
    'avgPrice': {},
    'depth20': {}
}


def processData(subsType, data):
    if subsType == 'kline_1s':
        data = data['k']

    letters = {
        'kline_1s': ['T', 'o', 'h', 'l', 'c', 'v', 'q', 'V', 'Q', 'n'],
        'ticker': ['P', 'p', 'w', 'x', 'c', 'Q', 'b', 'B', 'a', 'A', 'o', 'h', 'l', 'v', 'q', 'n', 'C'],
        'avgPrice': ['E', "w"],
        'depth20': ['bids', 'asks']
    }[subsType]

    return np.array([float(data[l]) for l in letters])


def display_message(_, message):
    message = json.loads(message)
    if 'stream' not in message:
        print(message)
        return
    subsType = message['stream'].split('@')[1]
    pair = message['stream'].split('@')[0]
    data[subsType][pair] = processData(subsType, message['data'])

    if subsType == 'kline_1s' and pair == 'btcusdt':
        print(data['kline_1s'][pair])
        print(data['ticker'][pair])
        print(data['avgPrice'][pair])
        print(data['depth20'][pair])
    # output = ''
    # for k, v in data.items():
    #     output += f'{k}: {len(v)}\n'
    # output_label.config(text=output)


root.mainloop()
