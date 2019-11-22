
import numpy as np

def CO_NonlinearAutocorr( y, taus, doAbs=None) :

    '''
    CO_NonlinearAutocorr   A custom nonlinear autocorrelation of a time series.

     Nonlinear autocorrelations are of the form:
     <x_i x_{i-\tau_1} x{i-\tau_2}...>
     The usual two-point autocorrelations are
     <x_i.x_{i-\tau}>

     Assumes that all the taus are much less than the length of the time
     series, N, so that the means can be approximated as the sample means and the
     standard deviations approximated as the sample standard deviations and so
     the z-scored time series can simply be used straight-up.

    ---INPUTS:
     y  -- should be the z-scored time series (Nx1 vector)
     taus -- should be a vector of the time delays as above (mx1 vector)
       e.g., [2] computes <x_i x_{i-2}>
       e.g., [1,2] computes <x_i x_{i-1} x{i-2}>
       e.g., [1,1,3] computes <x_i x_{i-1}^2 x{i-3}>
     doAbs [opt] -- a boolean (0,1) -- if one, takes an absolute value before
                    taking the final mean -- useful for an odd number of
                    contributions to the sum. Default is to do this for odd
                    numbers anyway, if not specified.

    ---NOTES:
     (*) For odd numbers of regressions (i.e., even number length
             taus vectors) the result will be near zero due to fluctuations
             below the mean; even for highly-correlated signals. (doAbs)

     (*) doAbs = 1 is really a different operation that can't be compared with
             the values obtained from taking doAbs = 0 (i.e., for odd lengths
             of taus)
    (*) It can be helpful to look at nlac at each iteration.
    '''

    if doAbs == None:

        if ((len(taus) % 2) == 1) : # use default settings for doAbs
            doAbs = False
        else :               # Even number of time lags
            doAbs = True     # take abs, otherwise will be a very small number

    N = len(y) # time series length

    tmax = np.max(taus) # maximum delay time

    nlac = y[tmax : N]

    for i in range(0, len(taus)):
        nlac = np.multiply(nlac, y[(tmax-taus[i]):(N-taus[i])], dtype=np.float64) # using default data type caused int overflow on third iteration, hence dtype=np.float64

    # COMPUTE OUTPUT

    if doAbs :
        out = np.mean(np.abs(nlac))
    else :
        out = np.mean(nlac)

    return out # output a bit different for very large input arrays, could be just rounding differences in mean for MATLAB vs Python
