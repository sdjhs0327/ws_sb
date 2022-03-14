import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from dateutil.relativedelta import relativedelta

def cal_return(srs_rets, term = "m"):
    '''연수익률 산출; 단위수익률 시리즈, 리벨런싱주기'''
    if term == 'm':
        rets = srs_rets.mean() * 12
    elif term == 'bit':
        ## 데이터가 빠지기는 하지만 거의 무중단을 가정함
        ## 시계열단위가 짧아 기하평균 수익률을 사용하는게 맞다고 판단함
        rets = (pow(((srs_rets+1).prod()), 1/len(srs_rets))-1)*24*365   
    else:
        rets = srs_rets.mean() * 250     
    return rets

def cal_volatility(srs_rets, term = 'm'):
    '''연변동성 산출; 단위수익률 시리즈, 리벨런싱주기'''
    if term == 'm':
        vols = np.sqrt(srs_rets.var()*12)
    elif term == 'bit':
        vols = np.sqrt(srs_rets.var()*(24*365))
    else:
        vols = np.sqrt(srs_rets.var()*250)
    return vols

def cal_sr(srs_rets, term = 'm'):
    '''Sharpe Ratio 산출; 단위수익률 시리즈, 리벨런싱주기'''
    if term == 'm':
        sr = cal_return(srs_rets, term = "m")/cal_volatility(srs_rets, term = 'm')
    elif term == 'bit':
        sr = cal_return(srs_rets, term = "bit")/cal_volatility(srs_rets, term = 'bit')
    else:
        sr = cal_return(srs_rets, term = "d")/cal_volatility(srs_rets, term = 'd')
    return sr

def cal_mdd(srs_rets):
    '''MDD 산출; 단위수익률 시리즈 '''
    arr_v = np.array((srs_rets + 1).cumprod())
    peak_l = np.argmax(np.maximum.accumulate(arr_v) - arr_v)
    peak_u = np.argmax(arr_v[:peak_l])
    return (arr_v[peak_l] - arr_v[peak_u]) / arr_v[peak_u]

def cal_wr(srs_rets):
    '''승률 산출; 단위수익률 시리즈'''
    wr = (srs_rets>=0).sum()/len(srs_rets)
    return wr

def get_report(srs_rets, term = 'm'):
    '''평가 리포트; 단위수익률 시리즈, 리벨런싱주기'''
    rets_ = cal_return(srs_rets, term)
    vols_ = cal_volatility(srs_rets, term)
    sr_ = rets_/vols_
    mdd_ = cal_mdd(srs_rets)
    wr_ = cal_wr(srs_rets)
    return pd.DataFrame([rets_, vols_, sr_, mdd_, wr_], index=['Return', 'Volatility', 'Sharpe', 'MDD', 'Win']).T.round(4)

def get_report2(df_rets, term = 'm'):
    '''자산(전략)별 평가; 단위수익률 테이블'''
    return pd.concat([get_report(df_rets[col], term) for col in df_rets.columns]).set_index(df_rets.columns)

def get_df_val(df_rets):
    '''수익률 > 가치 테이블 변환; 단위수익률 테이블'''
    df_value = (df_rets+1).cumprod()
    df_value.loc[df_value.index[0] - relativedelta(months=1)] = np.repeat(1, len(df_value.columns))   
    return df_value.sort_index()

def get_dd(df_value):
    '''전고점대비하락 테이블; 자산가치 테이블'''
    ls_dd = []
    for col in df_value.columns:
        srs = df_value[col]
        temp_ls = [srs[:i+1].max() for i in range(len(srs))]
        ls_dd.append(srs/temp_ls - 1)
    return pd.concat(ls_dd, axis=1)