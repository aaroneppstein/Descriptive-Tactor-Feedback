import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
from sklearn import metrics
import math

## Reading in the Data from CSV ##
file_5Tests = 'CleanedData/Cleaned_5Tests.csv'
csv_read_5Tests = pd.read_csv(file_5Tests)

df_raw = csv_read_5Tests.T.to_numpy()

data = df_raw[1:]
curr_data = data[0]
force_data = data[1]

## Linear Regression of Current v Force ##
results_lin = stats.linregress(curr_data,force_data)
pred_lin_force = results_lin.slope*curr_data + results_lin.intercept
print('R^2: {:.3f}, Std Dev: {:.3f}'.format(results_lin.rvalue,results_lin.stderr))

## RMSE, MAE, and Max Error of fit to data ##
MSE_lin = metrics.mean_squared_error(force_data, pred_lin_force)
RMSE_lin = math.sqrt(MSE_lin)
MAE_lin = metrics.mean_absolute_error(force_data,pred_lin_force)
max_error_lin = metrics.max_error(force_data,pred_lin_force)

print('Linear Fit: RMSE: {:.3f}, MAE: {:.3f}, Max Error: {:.3f}'.format(RMSE_lin,MAE_lin,max_error_lin))

## Plotting of data ##
plt.figure(dpi=144)
plt.plot(curr_data,force_data,label='Experimental Data',alpha=0.4)
plt.plot(curr_data,pred_lin_force,label='Linear Fit, R^2: {:.3f}'.format(results_lin.rvalue))
plt.xlabel('Current A')
plt.ylabel('Force N')
plt.title('Linear Fit of Current v Force')
plt.legend()

plt.show()

