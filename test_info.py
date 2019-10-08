
import rm_histogram2 as hist
import rm_information as info
import numpy as np
import co_rm_amInformation as co


x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
x2 = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
y = np.array([6, 7, 8, 9, 10, 6, 7, 8, 9])
print("arrays used for testing: ")
print("print x: ", x)
print("print y: ", y)
print()

#histogram test
print("rm_histogram2() test ------------------------")
result = hist.rm_histogram2(x, y)
print ("histogram: ", result[0])
print("descriptor: ", result[1])
print()

#information test
print("rm_information() test ------------------------")
info = info.rm_information(x, y)
print("estimate: ", info[0])
print("nbias: ", info[1])
print("sigma: ", info[2])
print("descriptor: ", info[3])
print()

#co information test
print("co_rm_amInformation() test---------------------" )
out = co.co_rm_amInformation(y)
print("estimate: ", out)
print()


