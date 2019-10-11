
import numpy as np
from operations import MD_pNN as pnn
from scipy import io

y1 = np.array([8, 3, 18, 9, 6, 2, 19, 20])
y2 = np.array([0.00004, 0.00008, 0.45, 0.00003, 0.00008])
y3 = np.array([0.0003, 6, 0.0009, 0.000008, 1])

data = io.loadmat("UVA0001_rr", squeeze_me = True)
rr = np.asarray(data['rr'])

print('houlter RR data')
out = pnn.MD_pNN(rr)
print(out)
print()

# how to import rr data, stolen from justins code
# mat = scipy.io.loadmat('/Users/justinniestroy-admin/Documents/Work/Randall Data/houlter data/RR/UVA' + id +'_rr.mat',squeeze_me=True)
#     rr = np.asarray(mat['rr'])

print("y1:")
out = pnn.MD_pNN(y1)
print(out)
print()

print('y2:')
out = pnn.MD_pNN(y2)
print(out)
print()

print('y3:')
out = pnn.MD_pNN(y3)
print(out)
