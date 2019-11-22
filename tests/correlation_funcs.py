import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from minio import Minio


def do_it_all(ids, vital, path = '',diff = False,down = True):
    if down:
        print("Downloading Data")
        download(ids,vital,path,diff)
    print("Making Dataframe for all Patients")
    df = make_df(ids,vital,diff)
    age_df = get_age_data(ids)
    df = add_post_age(df,age_df)
    speeds = get_algo_speeds()
    print("Calculating Correlations")
    results = make_plot(new_df_hr, speeds,'Correlation Betweem '+ vital + ' Algos and Post Menst Age','corr ' + vital)

    return results, df

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_algo_speeds():
    data = {'DN_Moments': 38.4,'DN_RemovePoints':32.55555, 'DN_Withinp': 18.08888888888889, 'DN_Quantile': 39.8, 'DN_OutlierInclude': 84.46666666666667, 'DN_Burstiness': 10.822222222222223, 'DN_pleft': 48.08888888888889, 'CO_FirstZero': 30.933333333333334, 'DN_Fit_mle': 7.444444444444445, 'CO_FirstMin': 22.91111111111111, 'DN_IQR': 48.82222222222222, 'DN_CompareKSFit': 19332.088888888888, 'DN_Mode': 48.55555555555556, 'EN_SampEn': 12418.68888888889,'EN_QuadEn': 12418.68888888889, 'SY_Trend': 195.73333333333332, 'DN_Mean': 1.8666666666666667,'DN_HighLowMu': 11.288889, 'CO_glscf': 66.0, 'DN_Cumulants': 62.93333333333333, 'DN_Range': 2.6, 'DN_FitKernalSmooth': 694.5777777777778, 'DN_Median': 15.377777777777778, 'DN_Spread': 7.555555555555555, 'DN_MinMax': 1.0, 'DN_CustomSkewness': 29.466666666666665, 'EN_mse': 14695.08888888889, 'IN_AutoMutualInfo': 34.48888888888889, 'EN_CID': 47.8, 'DN_Unique': 8.311111111111112, 'DT_IsSeasonal': 519.7111111111111, 'EN_ApEn': 5698.4, 'SC_HurstExp': 209.88888888888889, 'DN_ObsCount': 1.4666666666666666, 'EN_ShannonEn': 403.2888888888889, 'CO_tc3': 52.666666666666664, 'DN_nlogL_norm': 37.84444444444444, 'CO_AutoCorr': 27.488888888888887, 'CO_f1ecac': 31.022222222222222, 'DN_ProportionValues': 336.6666666666667, 'DN_STD': 7.5777777777777775, 'CO_trev': 33.46666666666667, 'DN_cv': 9.133333333333333, 'DN_TrimmedMean': 12.022222222222222, 'SC_DFA': 95408.66666666667, 'DN_HighLowMu': 11.28888888888889}
    speeds = pd.DataFrame(list(data.items()))
    speeds =  speeds.sort_values(by=[0]).rename(columns = {0:'Operation', 1:'Relative Time'}).reset_index(drop=True)
    return speeds

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def add_post_age(df,age_df):
    age_df['id'] = age_df['PatientID']
    new_df_hr = df_hr.merge(age_df[['id','GestAge','GestAgeDays']],how='left')
    new_df_hr['postmenst age'] = new_df_hr['GestAge']*7 + new_df_hr['days'] + new_df_hr['GestAgeDays']
    new_df_hr = new_df_hr.drop(columns=['Hurst Exp', 'DFA alpha','IsSeasonal?'])
    new_df_hr = new_df_hr[ new_df_hr['postmenst age'] < 40 * 7]
    return new_df_hr

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def make_df(ids,vital,diff):
    if diff:
        diffstr = 'fd_'
    else:
        diffstr = ''
    i = ids[0]
    df_hr = pd.read_csv(path + vital +  ' Results/UVA_' + str(i) + '_'+diffstr + vital + '.csv')
    df_hr['id'] = i
    for i in ids[1:]:
        try:
            df1 =  pd.read_csv(path + vital  + ' Results/UVA_' + str(i) + '_'+diffstr + vital + '.csv')
        except:
            continue
        df1['id'] = i
        frames = [df_hr, df1]

        df_hr = pd.concat(frames)
    df_hr['days'] = (df_hr['time'] / 60 / 60 /24).round()
    return df_hr

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def download(ids,vital,path,diff):
    minioClient = Minio('minionas.uvadcos.io',
                    access_key='breakfast',
                    secret_key='breakfast',
                    secure=False)
    if diff:
        diffstr = 'fd_'
    else:
        diffstr = ''
    for i in ids:
        obj_name = 'NICU Vitals/HCTSA Analysis2/UVA_' + str(i) + '/UVA_' + str(i) + '_'+ diffstr +vital+'.csv'
        try:
            data = minioClient.get_object('breakfast', obj_name)
        except:
            continue
        with open(path + vital + ' Results/UVA_' + str(i) + '_'+diffstr + vital + '.csv', 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_age_data(ids,path):
    base = path
    try:
        age_df = pd.read_csv(path + 'age_df.csv')
        return age_df
    except:
        file = 'UVA_' + str(ids[0]) + '_vitals.mat'
        arrays = {}
        f = h5py.File(base+file,'r')
        for k, v in f.items():
            arrays[k] = np.array(v)
        pname = get_column_names(f['pname'],f)
        pdata = arrays['pdata']
        pdata_dict = {}
        j = 0
        for name in pname:
            pdata_dict[name] = float(pdata[j])
            j = j + 1
        pdata_dict
        age_df = pd.DataFrame(pdata_dict,index=[0])
        for i in ids[1:]:
            file = 'UVA_' + str(i) + '_vitals.mat'
            arrays = {}
            f = h5py.File(base+file,'r')
            for k, v in f.items():
                arrays[k] = np.array(v)
            pname = get_column_names(f['pname'],f)
            pdata = arrays['pdata']
            pdata_dict = {}
            j = 0
            for name in pname:
                pdata_dict[name] = float(pdata[j])
                j = j + 1
            pdata_dict
            frames = [pd.DataFrame(pdata_dict,index=[0]),age_df]
            age_df = pd.concat(frames)
        return age_df

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import h5py

def read_in_NICU_file(path):
    arrays = {}
    f = h5py.File(path,'r')
    for k, v in f.items():
        arrays[k] = np.array(v)
    df = pd.DataFrame(np.transpose(arrays['vdata']))
    df = df.dropna(axis=1, how='all')
    df.columns = get_column_names(f['vname'],f)
    times = pd.Series(arrays['vt'][0], index=df.index)
    df['time'] = times

    return df

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_column_names(vname,f):
    names = []
    for name in vname[0]:
        obj = f[name]
        col_name = ''.join(chr(i) for i in obj[:])
        names.append(col_name)
    return names

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_max_corr(corrs):
    func_maxs = {}
    mx= 0
    for i in range(2,7):
        if corrs['Moment ' + str(i)] > mx:
            mx =  corrs['Moment ' + str(i)]
    func_maxs['DN_Moments'] = mx
    mx = 0
    for i in range(1,3):
        if corrs['Within ' + str(i) + ' std'] > mx:
            mx =  corrs['Within ' + str(i) + ' std']
    func_maxs['DN_Withinp'] = mx
    mx = 0
    for i in ['75','90','50','95','99']:
        if corrs['Quantile ' + str(i)] > mx:
            mx =  corrs['Quantile ' + str(i)]
    func_maxs['DN_Quantile'] = mx
    func_maxs['DN_OutlierInclude'] = 0
    func_maxs['DN_Burstiness'] = corrs['Burstiness']
    func_maxs['DN_pleft'] = corrs['pleft']
    func_maxs['CO_FirstZero'] = corrs['FirstZero']
    func_maxs['DN_Fit_mle'] = max(corrs['mean'],corrs['std'])
    func_maxs['CO_FirstMin'] = corrs['FirstMin']
    func_maxs['DN_IQR'] = corrs['iqr']
    func_maxs['DN_CompareKSFit'] = max(corrs['DN_CompareKSFit adiff'],corrs['DN_CompareKSFit peaksepy'],corrs['DN_CompareKSFit relent'])
    func_maxs['DN_Mode'] = corrs['mode']
    func_maxs['EN_SampEn'] = corrs['Sample Entropy']
    func_maxs['EN_QuadEn'] = corrs['Quadratic Entropy']
    func_maxs['SY_Trend'] = max(corrs['Trend gradient'],corrs['Trend interceptYC'],corrs['Trend meanYC22'],corrs['Trend meanYC'],\
                           corrs['Trend meanYC12'],corrs['Trend stdRatio'] ,corrs['Trend stdYC']   )
    func_maxs['DN_Mean'] = corrs['mean']
    func_maxs['CO_glscf'] = 0
    func_maxs['DN_Cumulants'] = corrs['std']
    func_maxs['DN_Range'] = corrs['range']
    func_maxs['DN_FitKernalSmooth'] = 0
    func_maxs['DN_Median'] = corrs['median']
    func_maxs['DN_Spread'] = max(corrs['Median Abs Deviation'],corrs['Mean Abs Deviation'])
    func_maxs['DN_MinMax'] = max(corrs['min'],corrs['max'])
    func_maxs['DN_CustomSkewness'] = corrs['Pearson Skew']
    func_maxs['EN_mse'] = 0
    func_maxs['IN_AutoMutualInfo'] = corrs['Auto Mutual Info Auto Mutual 1']
    func_maxs['EN_CID'] = max(corrs['Complexity CE2_norm'],corrs['Complexity CE2'],corrs['Complexity CE1_norm'],\
                             corrs['Complexity CE1'],corrs['Complexity minCE2'],corrs['Complexity minCE1'])
    func_maxs['DN_Unique'] = corrs['Percent Unique']
    func_maxs['DT_IsSeasonal'] = 0
    func_maxs['EN_ApEn'] = corrs['ApEn']
    func_maxs['SC_HurstExp'] = 0
    func_maxs['DN_ObsCount'] = corrs['Observations']
    func_maxs['EN_ShannonEn'] = corrs['Shannon Entropy']
    func_maxs['CO_tc3'] = corrs['tc3']
    func_maxs['DN_nlogL_norm'] = corrs['Log liklihood of Norm fit']
    mx= 0
    for i in range(1,26):
        if corrs['AutoCorr lag ' + str(i)] > mx:
            mx =  corrs['AutoCorr lag ' + str(i)]
    func_maxs['CO_AutoCorr'] = mx
    func_maxs['CO_f1ecac'] = corrs['f1ecac']
    func_maxs['DN_ProportionValues'] = 0
    func_maxs['DN_STD'] = corrs['std']
    func_maxs['CO_trev'] = corrs['trev']
    func_maxs['DN_cv'] = max(corrs['DN_cv 3'],corrs['DN_cv 2'],corrs['DN_cv 1'])
    func_maxs['DN_TrimmedMean'] = max(corrs['trimmed mean 25'],corrs['trimmed mean 50'],corrs['trimmed mean 75'])
    func_maxs['SC_DFA'] = 0
    func_maxs['DN_HighLowMu'] = corrs['High Low Mean Ratio']
    func_maxs['DN_RemovePoints'] = max(corrs['DN_RemovePoints ac2rat'],corrs['DN_RemovePoints kurtosisrat'],corrs['DN_RemovePoints skewnessrat'],corrs['DN_RemovePoints fzcacrat'],\
           corrs['DN_RemovePoints std'] , corrs['DN_RemovePoints median'],corrs['DN_RemovePoints mean'])
    return(func_maxs)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def make_plot(df,speeds,title = 'Test',name = 'corr-test'):
    import matplotlib
    import matplotlib.pyplot as plt

    correlations = find_corrs(df)

    max_corrs = pd.DataFrame(list(get_max_corr(correlations).items())).sort_values(by=[0]).rename(columns = {0:'Operation', 1:'Corr'}).reset_index(drop=True)
    both = speeds
    pd.set_option('display.max_rows', 44)
    both['Correlation'] = max_corrs['Corr']
    matplotlib.rc('xtick', labelsize=5)
    matplotlib.rc('ytick', labelsize=5)
    matplotlib.rcParams.update({'font.size': 7})
    j = 1
    for i in range(len(both)):


        x = np.log2(both['Relative Time'][i])
        y = both['Correlation'][i]

        if y == 0:
            plt.plot(x, y,'ro')
            if x > 10:
                plt.text(x * (1 + j* 0.01), y + .01*j , both['Operation'][i], fontsize=4)
                if x < 10:
                    j = j
            continue

        plt.plot(x, y,'bo')
        if y > .2 or x > 7:
            plt.text(x * (1 + j* 0.03), y * (1 + j*0.03) , both['Operation'][i], fontsize=4)

    plt.xlim((-.1, 17))
    plt.xlabel("Log of Time to run")
    plt.ylim((-.1, .45))
    plt.ylabel("Correlation with Age")
    plt.title(title)
    plt.savefig(path + name+ ".png",dpi = 500)
    plt.show()
    return both

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def find_corrs(df):
    correlations = {}
    for col in df.columns:
        if col == 'time'or col == 'days' or col == 'id' or col == 'GestAge' or col == 'GestAgeDays' or col == 'postmenst age':
            continue
        result = df[col].corr(df['postmenst age'])
        if np.isnan(result):
            sample = np.asarray(df[pd.notna(df[col])][col])
            days = df[pd.notna(df[col])]['postmenst age']
            result = np.corrcoef(sample[1:27000],days[1:27000])[1,0]
            if np.isnan(result):
                result = 0
        correlations[col] = np.absolute(result)
    return correlations
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
