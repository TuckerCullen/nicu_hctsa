
# from justin's github

import numpy as np
import math

def CO_AutoCorr(y,lag = 1,method = 'TimeDomianStat',t=1):
    # if not isinstance(y,np.ndarray):
    #     y = np.asarray(y)
    if method == 'TimeDomianStat':
        if lag == []:
            acf = [1]
            for i in range(1,len(y)-1):
                acf.append(np.corrcoef(y[:-lag],y[lag:])[0,1])
            return acf
        return(np.corrcoef(y[:-lag],y[lag:])[0,1])

    # if method == 'Fourier':

    # MATLAB CODE FOR 'Fourier' case

    # nFFT = 2^(nextpow2(N)+1);
    # F = fft(y - mean(y),nFFT);
    # F = F.*conj(F);
    # acf = ifft(F); % Wiener?Khinchin
    # acf = acf./acf(1); % Normalize
    # acf = real(acf);
    # acf = acf(1:N);
    #
    # if isempty(tau) % return the full function
    #     out = acf;
    # else % return a specific set of values
    #     out = zeros(length(tau),1);
    #     for i = 1:length(tau)
    #         if (tau(i) > length(acf)-1) || (tau(i) < 0)
    #             out(i) = NaN;
    #         else
    #             out(i) = acf(tau(i)+1);
    #         end
    #     end
    # end


    else:
        N = len(y)
        nFFT = int(2**(np.ceil(np.log2(N)) + 1))
        F = np.fft.fft(y - y.mean(),nFFT)
        F = np.multiply(F,np.conj(F))
        acf = np.fft.ifft(F)
        if acf[0] == 0:
            if lag == []:
                return acf
            return acf[lag]


        acf = acf / acf[0]
        acf = acf.real
        if lag == []:
            return acf
        return acf[lag]
