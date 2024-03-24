import h5py
import numpy as np

def addData(pair, date, data):
    with h5py.File('datasets/data.h5', 'a') as file:
        if pair not in file:
            pair_group = file.create_group(pair)
        else:
            pair_group = file[pair]

        if date in pair_group:
            existing_data = pair_group[date][:]
            del pair_group[date]
            combined_data = np.concatenate((existing_data, data))
        else:
            combined_data = data
        maxshape = (None,) if len(combined_data.shape) == 1 else (None, combined_data.shape[1])
        pair_group.create_dataset(date, data=combined_data, chunks=True, maxshape=maxshape)


addData('BTC-USDT', '06-01-2021', np.random.rand(2))

def showData(pair, date):
    with h5py.File('datasets/data.h5', 'r') as file:
        if pair in file:
            pair_group = file[pair]
            if date in pair_group:
                data = pair_group[date][:]
                print(f'{pair} - {date}: {data}')
            else:
                print(f"No data for date {date} in pair {pair}")
        else:
            print(f"No data for pair {pair}")

showData('BTC-USDT', '06-01-2021')

