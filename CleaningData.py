import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats

## Reading in the Data from CSV ##
file = 'FinalData_Collection_FINAL.csv'
csv_read = pd.read_csv(file)

df_raw = csv_read.T.to_numpy()

data = df_raw[1:]
curr_data = data[0][1:]      #First value of array is 0
lc_data = data[1][1:]
samp_rate = 40000
samp_time = 5
samp_bin = samp_rate*samp_time
bin_size = 10000

## Moving Average ##

curr_data_avg = []
lc_data_avg = []

# Current Moving Average
i = 0
while i < len(curr_data) - bin_size + 1:
      
    # Calculate the average of current window
    curr_window_average = np.sum(curr_data[i:i+bin_size]) / bin_size
    # window in moving average lis
    curr_data_avg.append(curr_window_average)
      
    # Shift window to right by one position
    i += 1
curr_data_avg = np.array(curr_data_avg)

# Load Cell Moving Average
i = 0
while i < len(lc_data) - bin_size + 1:
      
    # Calculate the average of current window
    lc_window_average = np.sum(lc_data[i:i+bin_size]) / bin_size
      
    # window in moving average lis
    lc_data_avg.append(lc_window_average)
      
    # Shift window to right by one position
    i += 1
lc_data_avg = np.array(lc_data_avg)

# Current Conversion
conv_fact = 1/0.4            # Conversion factor of 400 mV/A which can also be said as 2.5 A/V
Vref = 2.5                   # Vcc / 2

curr_avgd = conv_fact*(Vref-curr_data_avg)                   

# Load Cell Conversion
slope = 194477.613586                           # From Calibration Curve 6-2 (Load Cell Calibrated Day of Testing)
intercept = -27.78270265
lc_avgd = lc_data_avg*slope + intercept

lc_avgd = lc_avgd + np.abs(np.min(lc_avgd))     # Weirdly zeroed at -400 g no matter what I did
lc_avgd = lc_avgd*(9.8/1000)                    # Converting to force from grams from calibration curve


def slice_and_avg(data,test_num):               # Slicing the data into the number of tests and averaging it whole
    reshaped = np.reshape(data[1:],(test_num,len(data)//test_num))
    avg = np.mean(reshaped,axis=0)
    return avg

curr_full_avg = slice_and_avg(curr_avgd,5)      # Five Tests were performed
lc_full_avg = slice_and_avg(lc_avgd,5)          # Five Tests were performed

corr_full_avg, _ = stats.pearsonr(lc_full_avg,curr_full_avg)        # Pearsons Correlation
print('Pearsons correlation: %.3f' % corr_full_avg)

### Outputting Cleaned Up Data to CSV ###
avg_5_tests= np.vstack((curr_avgd,lc_avgd))
avg_5_tests_df = pd.DataFrame(avg_5_tests.T,columns=['Current Sensor', 'Load Cell'])
avg_5_tests_df.to_csv('CleanedData/Cleaned_5Tests.csv')
avg_full = np.vstack((curr_full_avg, lc_full_avg))
avg_full_df = pd.DataFrame(avg_full.T,columns=['Current Sensor', 'Load Cell'])
avg_full_df.to_csv('CleanedData/Cleaned_fullAvg.csv')


### Plotting Data for Visual ###

## Raw Data
'''plt.figure(figsize=(8,12),dpi=144)
plt.suptitle('Raw Data')
plt.subplot(2,1,1)
plt.plot(curr_data)
plt.xlabel('Samples')
plt.ylabel('Voltage V')

plt.subplot(2,1,2)
plt.plot(lc_data)
plt.xlabel('Samples')
plt.ylabel('Voltage V')'''

## Moving Average of Data
plt.figure(figsize=(8,12),dpi=144)
plt.suptitle('Moving Average of {} for all 5 Tests'.format(bin_size))
plt.subplot(2,1,1)
plt.plot(curr_avgd)
plt.xlabel('Samples')
plt.ylabel('Current A')

plt.subplot(2,1,2)
plt.plot(lc_avgd)
plt.xlabel('Samples')
plt.ylabel('Force N')
plt.savefig('plots/MovAvg_5Tests.png')

## Force v Current all 5
plt.figure(dpi=144)
plt.title('Current v Force Hysteresis of all 5 Tests')
plt.plot(curr_avgd,lc_avgd)
plt.ylabel('Force N')
plt.xlabel('Current A')
plt.savefig('plots/Hyst_5Tests.png')

## All data averaged together
plt.figure(figsize=(8,12),dpi=144)
plt.suptitle('All 5 Tests averaged together')
plt.subplot(2,1,1)
plt.plot(curr_full_avg)
plt.xlabel('Samples')
plt.ylabel('Current A')

plt.subplot(2,1,2)
plt.plot(lc_full_avg)
plt.xlabel('Samples')
plt.ylabel('Force N')
plt.savefig('plots/MovAvg_AvgTogether.png')

## Force v Current Hysteresis
plt.figure(dpi=144)
plt.title('Current v Force Hysteresis Averaged')
plt.plot(curr_full_avg,lc_full_avg)
plt.ylabel('Force N')
plt.xlabel('Current A')
plt.savefig('plots/Hyst_AvgTogether.png')

plt.show()


