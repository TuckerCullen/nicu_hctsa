
from operations import SB_CoarseGrain as cg
import numpy as np
import random
from operations import FC_Suprise as sup
import scipy as sc
from scipy import io

y1 = np.array([8, 3, 18, 9, 6, 2, 19, 20])

data = io.loadmat("UVA0001_rr", squeeze_me = True)
rr = np.asarray(data['rr'])

rs = io.loadmat('rs_var.mat', squeeze_me = False)
# print(rs)

# print('updown test')
# yth1 = cg.SB_CoarseGrain(y1, "updown", 10)
# print('yth1: ', yth1)
# print()
#
# print('embed2quadrants test, also tau test')
# yth2 = cg.SB_CoarseGrain(y1, "embed2quadrants", 'tau')
# print('yth2: ', yth2)
# print()

# print('quantile test')
# yth3 = cg.SB_CoarseGrain(y1, "quantile", 3)
# print(yth3)
# print()

# print("Test BF_resetSeed")
# rs.BF_ResetSeed('none')
# print("random number: ", random.randint(1, 10))

print("Test FC Suprise Default")
out1 = sup.FC_Suprise(rr)
print("out1: ", out1)
print()

# print("T1 Test")
# out3 = sup.FC_Suprise(rr, whatPrior='T1')
# print("out3: ", out3)
# print()

# print("T2 Test")
# out4 = sup.FC_Suprise(rr, whatPrior='T2')
# print("out4: ", out4)
# print()














