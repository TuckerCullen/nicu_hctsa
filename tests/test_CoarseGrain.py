
from operations import SB_CoarseGrain as cg
from periphery_functions import BF_ResetSeed as rs
import numpy as np
import random

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
print()

print("Test BF_resetSeed")
rs.BF_ResetSeed('none')
print("random number: ", random.randint(1, 10))

