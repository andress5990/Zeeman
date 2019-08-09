import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import statistics as st

from scipy import stats

import pdb

def Calc_Deltas(Data_list, step):
    Deltas = []
    for count in range(len(Data_list)):
        if count >= step and count <= len(Data_list):
            delta = Data_list[count] - Data_list[count-step] 
            Deltas.append(delta)
    return Deltas
        
def Stats(Data_list):
   
    mean_data = st.mean(Data_list)
    std_data = st.stdev(Data_list)
    return [mean_data, std_data]

def Linear_Model(Data_list):
    
    x = np.arange(0, len(Data_list), step=1)
    [slope, intercept, r_value, p_value, std_err] = stats.linregress(x,Data_list)
    
    return [slope, intercept, r_value, p_value, std_err, x]
    
def Linear_Func(intercept, slope, time_list):
    f_fit = []
    for time in time_list:
        f = slope*time + intercept
        f_fit.append(f)
    
    return f_fit
    
    
    

file_name = str(sys.argv[1])
step = 1

reader = pd.ExcelFile(file_name)
sheetlist = reader.sheet_names

df1 = pd.read_excel(file_name, sheet_name=sheetlist[2], header=None, usecols="A, B")
df1_headers = df1.head(0)
df2 = pd.read_excel(file_name, sheet_name=sheetlist[3], header=None, usecols="A, B")
df2_headers = df2.head(0)
df3 = pd.read_excel(file_name, sheet_name=sheetlist[4], header=None, usecols="A, B")
df3_headers = df2.head(0)

t_Z_OFF_I = []
t_Z_ON = []

t_Z_OFF_F = []
f_Z_OFF_I = []

f_Z_ON = []
f_Z_OFF_F = []

# Cargamos los datos en las listas
for data in range(len(df1[0])):
    t_Z_OFF_I.append(df1[0][data])
    f_Z_OFF_I.append(df1[1][data])

for data in range(len(df2[0])):
    t_Z_ON.append(df2[0][data])
    f_Z_ON.append(df2[1][data])

for data in range(len(df3[0])):
    t_Z_OFF_F.append(df3[0][data])
    f_Z_OFF_F.append(df3[1][data])


Deltas = Calc_Deltas(f_Z_OFF_I, step) #calculamos los deltasf
[mean_delta, std_delta] = Stats(Deltas)#calculamos el promedio y la ds de los deltaf
[slope, intercept, r_value, p_value, std_err, time_list] = Linear_Model(f_Z_OFF_I)#minimos cuadrados
f_model = Linear_Func(intercept, slope, time_list)
                                                                         


#pdb.set_trace()

#  Graficamos los datos como vienen del archivo
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.set_ylim(min(f_Z_OFF_I), max(f_Z_OFF_I) + 0.2)
plt.xticks(np.arange(0, len(f_Z_OFF_I), step=60), fontsize=8)
plt.yticks(np.arange(min(f_Z_OFF_I), max(f_Z_OFF_I) + 0.2, step=0.1), fontsize=8)
ax1.set_xlabel("time(s)", fontsize=6)
ax1.set_ylabel("Delta Frequency (Hz)", fontsize=6)
ax1.grid()

ax1.plot(np.arange(0, len(f_Z_OFF_I)), f_Z_OFF_I)
ax1.plot(time_list, f_model)


plt.show()
