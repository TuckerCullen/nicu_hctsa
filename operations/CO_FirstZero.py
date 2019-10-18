
#from justin's github
from operations import CO_AutoCorr as ac

def CO_FirstZero(y, corrFun = 'ac'):
    acf = ac.CO_AutoCorr(y,[],'Fourier')
    N = len(y)
    for i in range(1,N-1):
        if acf[i] < 0:
            return i
    return N
