from time import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats

file = 'CSV_files/LoadCell_Data3.csv'
csv_read = pd.read_csv(file)

df_raw = csv_read.T.to_numpy()

data = df_raw[1:]
data = data[0][1:]      #First value of array is 0
samp_rate = 40000
samp_time = 5
samp_bin = samp_rate*samp_time
bin_size = 5000

weights = [0,100,200,500,1000,1400]

data_avg = []


## Moving Average ##
i = 0
while i < len(data) - bin_size + 1:
      
    # Calculate the average of current window
    window_average = np.sum(data[i:i+bin_size]) / bin_size
      
    # window in moving average lis
    data_avg.append(window_average)
      
    # Shift window to right by one position
    i += 1

data_avg_group = [np.mean(data_avg[samp_rate:samp_bin-samp_rate]),np.mean(data_avg[(samp_bin+samp_rate):(2*samp_bin)-samp_rate]),
                np.mean(data_avg[(2*samp_bin+samp_rate):(3*samp_bin)-samp_rate]), np.mean(data_avg[(3*samp_bin+samp_rate):(4*samp_bin)-samp_rate]),
                np.mean(data_avg[(4*samp_bin+samp_rate):(5*samp_bin)-samp_rate]), np.mean(data_avg[(5*samp_bin+samp_rate):(6*samp_bin)-samp_rate])]

fit_vals = stats.linregress(data_avg_group,weights)
print('Intercept = {}, Slope = {}'.format(fit_vals.intercept,fit_vals.slope))

plt.figure()
plt.plot(data_avg_group,weights,label='Cali Curve: y = {} x + {}'.format(fit_vals.slope,fit_vals.intercept))
plt.title('Weights and their corresponding Voltages')
plt.ylabel('Weight (g)')
plt.xlabel('Voltage (V)')
plt.legend(loc='best')

plt.figure()
plt.plot(data_avg)
plt.show()

    

