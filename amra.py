# -*- coding: utf-8 -*-
# ʱ������ARMAȥԤ������ķ
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# tsa��ģ��
from statsmodels.tsa.arima_model import ARMA
import warnings
from itertools import product
from datetime import datetime, timedelta
import calendar

warnings.filterwarnings('ignore')
# ���ݼ���, ����ķ���ݼ���
df = pd.read_csv('./002621.csv')
df = df[['time', 'prices']]

# ��ʱ����Ϊdf������
df.time = pd.to_datetime(df.time)
df.index = df.time
# ����̽��
print(df.head())
# ������
df_month = df.resample('M').mean()
# ������
df_Q = df.resample('Q-DEC').mean()
#����
df_year = df.resample('A-DEC').mean()
print(df_month)
#print(df_Q)
#print(df_year)

# �����죬�£����ȣ�������ʾ����ķָ��������
fig = plt.figure(figsize=[15, 7])
plt.rcParams['font.sans-serif']=['SimHei'] 
#����������ʾ���ı�ǩ
plt.suptitle('����ķָ��', fontsize=20)
plt.subplot(221)
plt.plot(df.prices, '-', label='����')
plt.legend()
plt.subplot(222)
plt.plot(df_month.prices, '-', label='����')
plt.legend()
plt.subplot(223)
plt.plot(df_Q.prices, '-', label='������')
plt.legend()
plt.subplot(224)
plt.plot(df_year.prices, '-', label='����')
plt.legend()
plt.show()

# ���ò�����Χ
ps = range(0, 3)
qs = range(0, 3)
parameters = product(ps, qs)
parameters_list = list(parameters)
# Ѱ������ARMAģ�Ͳ�������best_aic��С
results = []
best_aic = float("inf") # ������
for param in parameters_list:
    try:
        model = ARMA(df_month.prices,order=(param[0], param[1])).fit()
    except ValueError:
        print('��������:', param)
        continue
    aic = model.aic
    if aic < best_aic:
        best_model = model
        best_aic = aic
        best_param = param
    results.append([param, model.aic])

    # �������ģ��
print('����ģ��: ', best_model.summary())

# ����future_month����ҪԤ���ʱ��date_list
df_month2 = df_month[['prices']]
# ����������
future_month = 3
last_month = pd.to_datetime(df_month2.index[len(df_month2)-1])
#print(last_month)
date_list = []
for i in range(future_month):
    # �����¸����ж�����
    year = last_month.year
    month = last_month.month
    if month == 12:
        month = 1
        year = year+1
    else:
        month = month + 1
    next_month_days = calendar.monthrange(year, month)[1]
    #print(next_month_days)
    last_month = last_month + timedelta(days=next_month_days)
    date_list.append(last_month)
print('date_list=', date_list)

# ���δ��ҪԤ���3����
future = pd.DataFrame(index=date_list, columns= df_month.columns)
df_month2 = pd.concat([df_month2, future])
df_month2['forecast'] = best_model.predict(start=0, end=len(df_month2))
# ��һ��Ԫ�ز���ȷ������ΪNaN
df_month2['forecast'][0] = np.NaN
print(df_month2)

# ����ķָ��Ԥ������ʾ
plt.figure(figsize=(30,7))
df_month2.prices.plot(label='ʵ��ָ��')
df_month2.forecast.plot(color='r', ls='--', label='Ԥ��ָ��')
plt.legend()
plt.title('����ķָ�����£�')
plt.xlabel('ʱ��')
plt.ylabel('ָ��')
plt.show()