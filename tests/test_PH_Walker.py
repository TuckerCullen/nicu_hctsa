
import numpy as np
from scipy import io
from operations import PH_Walker as walk

y1 = np.array([8, 3, 18, 9, 6, 2, 19, 20])
y2 = np.array([9, 4, 19, 10, 7, 3, 20, 21])

# sub = np.mean(abs(y1-y2))

# print(sub)


data = io.loadmat("UVA0001_rr", squeeze_me = True)
rr = np.asarray(data['rr'])

out = walk.PH_Walker(rr, 'prop')

print(out)
