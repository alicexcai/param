import h5py
import numpy as np

hf = h5py.File('/Users/alicecai/Desktop/csecon/param/pypet/pypet/pypet-master/hdf5/trajectory.hdf5', 'r')
print('keys', hf.keys())
print('values', hf.values())
print('items', hf.items())
print(hf.__dict__)
# <h5py.h5f.FileID object at 0x7f93806e76b0>.dir()