
from operations import SB_CoarseGrain as cg
import numpy as np

y1 = np.array([8, 3, 18, 9, 6, 2, 19, 20])

print('updown test')
yth1 = cg.SB_CoarseGrain(y1, "updown", 10)
print('yth1: ', yth1)
print()

print('embed2quadrants test, also tau test')
yth2 = cg.SB_CoarseGrain(y1, "embed2quadrants", 'tau')
print('yth2: ', yth2)
print()

print('quantile test')
yth3 = cg.SB_CoarseGrain(y1, "quantile", 10)
print(yth3)
