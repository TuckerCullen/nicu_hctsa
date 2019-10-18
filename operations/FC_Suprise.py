
import numpy as np
from operations import SB_CoarseGrain as cg
from periphery_functions import BF_ResetSeed as reset

# WORK IN PROGRESS!!!!!!!! HAS NOT BEEN TESTED 

def FC_Suprise( y, whatPrior='dist', memory=0.2, numGroups=3, coarseGrainMethod='quantile', numIters=500, randomSeed=np.array([])):
    '''
    How surprised you would be of the next data point given recent memory.

    Coarse-grains the time series, turning it into a sequence of symbols of a
    given alphabet size, numGroups, and quantifies measures of surprise of a
    process with local memory of the past memory values of the symbolic string.

    We then consider a memory length, memory, of the time series, and
    use the data in the proceeding memory samples to inform our expectations of
    the following sample.

    The 'information gained', log(1/p), at each sample using expectations
    calculated from the previous memory samples, is estimated.


    :param y: the input time series
    :param whatPrior: the type of information to store in memory
            (i) 'dist' : the values of the time series in the previous memory
            (ii) 'T1' : the one-point transition probabiltiites in the pervious memory samples
            (iii) 'T2' : the two point transition probabilties in the memory samples

    :param memory: the memory length (either number of samples, or a proportion of the time-series length, if between 0 and 1
    :param numGroups: the number of groups to coarse-grain the time series into
    :param coarseGrainMethod: the coarse-graining, or symbolization method
            (i) 'quantile' : an equiprobable alphabet by the value of each time series datapoint
            (ii) 'updown' : an equiprobable alphabet by the value of incremental changes in the time-series values
            (iii) 'embed2quadrants' : 4-letter alphabet of the quadrant each data point resides in a two-dimensional embedding space

    :param numIters: the number of interations to repeat the procedure for
    :param randomSeed: whether (and how) to reset the random seed, using BF_ResetSeed
    :return: tuple containing summaries of this series of information gains, including: minimum, maximum, mean, median, lower and upper quartiles, and standard deviation
    '''

    # Check inputs and set defaults -- most defaults were set in the function declaration above ---------------------------------------------------------

    if (memory > 0) and (memory < 1): #specify memory as a proportion of the time series length
        memory = np.round(memory*len(y))


    # COURSE GRAIN ----------------------------------------------------------------------------------------------------------------

    yth = cg.SB_CoarseGrain(y, coarseGrainMethod, numGroups) # a coarse-grained time series using the numbers 1:numgroups

    N = len(yth)

    #select random samples to test
    reset.BF_ResetSeed(randomSeed)
    rs = np.random.permutation(N-memory) + memory # can't do beginning of time series, up to memory
    rs = np.sort(rs[0:min(numIters,(len(rs)-1))])

    # compute empirical probabilities
    store = np.zeros([numIters, 1])

    for i in range(0, len(rs)-1):
        if whatPrior == 'dist':
            # uses the distribution up to memory to inform the next point

            #calculate probability of this given past memory
            p = np.sum(yth[rs[i]-memory:rs[i]-1] == yth[rs[i]])/memory # needs testing, directly translated from matlab
            store[i] = p
        elif whatPrior == 'T1':
            # uses one-point correlations in memory to inform the next point

            # estimate transition probabilites from data in memory
            #find where in memory this has been obserbed before, and preceeded it

            memoryData = yth[rs[i] - memory:rs[i]-1]

            #previous data observed in memory here
            inmem = np.argwhere(memoryData[0:len(memoryData)-2] == yth[rs[i]])

            if inmem.size == 0:
                p = 0
            else:
                p = np.mean(memoryData[inmem+1] == yth[rs[i]])

            store[i] = p

        elif whatPrior == 'T2':

            # uses two point correlations in memory to inform the next point

            memoryData = yth[rs[i] - memory:rs[i]-1]
            inmem1 = np.argwhere(memoryData[1:memoryData.size-1] == yth[rs[i]-2])
            inmem2 = np.argwhere(memoryData[inmem1] == yth[rs[i]-2])

            if inmem2.size == 0:
                p = 0
            else:
                p = np.sum(memoryData[inmem2+2] == yth[rs[i]])/len(inmem2)

            store[i] = p

        else:
            print("Error: unknown method: " + whatPrior)

    # INFORMATION GAINED FROM NEXT OBSERVATION IS log(1/p) = -log(p)

    store[store == 0] = 1 # so that we set log[0] == 0


    ## STOPPED HERE ---------------------------------------------------------









