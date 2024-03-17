import h5py
import numpy as np

hdf5_file_path = 'datasets/your_file.h5'

new_data = np.random.rand(100)

with h5py.File(hdf5_file_path, 'a') as file:
    if 'your_dataset_name' in file:
        dataset = file['your_dataset_name']
        new_size = dataset.shape[0] + new_data.shape[0]
        dataset.resize(new_size, axis=0)
        dataset[-new_data.shape[0]:] = new_data
    else:
        dataset = file.create_dataset('your_dataset_name', data=new_data, maxshape=(None,))

    read_data = dataset[:]

