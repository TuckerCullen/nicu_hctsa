import numpy as np
import rm_information as info


def co_rm_amInformation(*args):
    """
    A wrapper for rm_information(), which calculates automutal information

    Inputs:
        y, the input time series
        tau, the time lag at which to calculate automutal information

    :returns estimate of mutual information

    - Wrapper initially developed by Ben D. Fulcher in MATLAB
    - rm_information.py initially developed by Rudy Moddemeijer in MATLAB
    - Translated to python by Tucker Cullen

    """
    nargin = len(args)

    y = args[0]

    if nargin == 2:
        tau = args[1]
    else:
        tau = 1  # default is to calculate the automutal info at lag 1

    if tau >= len(y):
        print("Time series two short for given time lag ", tau)
        return

    y1 = y[0: len(y) - tau]
    y2 = y[tau: len(y)]

    print("y1: ", y1) #just for testing purposes, can delete later
    print("y2: ", y2)

    out = info.rm_information(y1, y2)  # returns a tuple that includes all the outputs of rm_information.py

    return out[0]
