
from operations import MD_hrv_classic as hrv
import numpy as np

y = np.array([8, 3, 18, 9, 6, 2, 19])

out = hrv.MD_hrv_classic(y)

print()
print(out)
