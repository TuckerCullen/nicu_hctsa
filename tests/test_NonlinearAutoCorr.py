
import numpy as np
from scipy import io
from operations import CO_NonlinearAutocorr as na

y1 = np.array([8, 3, 18, 9, 6, 2, 19, 20])
y2 = np.array([9, 4, 19, 10, 7, 3, 20, 21])

data = io.loadmat("UVA0001_rr", squeeze_me = True)
rr = np.asarray(data['rr'])

out = na.CO_NonlinearAutocorr(rr, np.array([1, 1, 3]))

print(out)
