import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import statistics as st
import matplotlib.transforms as mtransforms

from scipy import stats

import pdb

def Calc_Deltas(Data_list, step):
    Deltas = []
    for count in range(len(Data_list)):
        if count >= step and count <= len(Data_list):
            delta = Data_list[count] - Data_list[count-step] 
            Deltas.append(delta)
    return Deltas

def Calc_PositiveDelta(Data_list, step):
    select_Dat = []
    time = []
    count = 0
    for count in range(len(Data_list)):
        if count >= step and count <= len(Data_list):
            delta = Data_list[count] - Data_list[count-step] 
            if delta <= 0:
                select_Dat.append(Data_list[count])
                time.append(count)
                count +=1
                
    return [time, select_Dat]
    
    
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

def Selection_Data(f_model, Data_list, std_err):   
    f_selection = []
    t_selection = []
    t = 0
    upperlim_list = []
    lowerlim_list = []
    
    for i in range(len(f_model)):
        upper_lim = f_model[i] + std_err
        lower_lim = f_model[i] - std_err
        if  Data_list[i] <= upper_lim and Data_list[i] >= lower_lim:
        #if  Data_list[i] <= up_lim:
            f_selection.append(Data_list[i])
            upperlim_list.append(upper_lim)
            lowerlim_list.append(lower_lim)
            t_selection.append(t)
            t += 1
    
    return [t_selection, f_selection, upperlim_list, lowerlim_list]
    

file_name = str(sys.argv[1])
step = 1
#step2 = 1
selection_factor = 5

#step = sys.argv[2]
#selection_factor = sys.argv[3]

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

Data_list_1 = f_Z_OFF_I

Deltas = Calc_Deltas(Data_list_1, step) #calculamos los deltasf
[mean_delta, std_delta] = Stats(Deltas)#calculamos el promedio y la ds de los deltaf
[slope, intercept, r_value, p_value, std_err, time_list] = Linear_Model(Data_list_1)#minimos cuadrados
f_model = Linear_Func(intercept, slope, time_list)#generamos la curva de ajuste 
[t_selection, f_selection, upperlim_list, lowerlim_list] = Selection_Data(f_model, Data_list_1, selection_factor*std_delta)
#seleccionamos los datos segun los limites escogidos, com referencia central a f_model, y una region circundante
# de factor*std_delta


#Hacemos el ajuste con los datos nuevos
#volvemos a crear un ajuste para los datos seleccionados
[slope2, intercept2, r_value2, p_value2, std_err2, time_list2] = Linear_Model(f_selection)#minimos cuadrados
f_model2 = Linear_Func(intercept2, slope2, time_list2)#creamos la curva de ajuste


#[time_list2, f_selection2] = Calc_PositiveDelta(Data_list_1, step2)                                                                        


#pdb.set_trace()

#  Graficamos los datos como vienen del archivo
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.set_ylim(min(f_Z_OFF_I), max(f_Z_OFF_I) + 0.2)
plt.xticks(np.arange(0, len(f_Z_OFF_I), step=20), fontsize=8)
plt.yticks(np.arange(min(f_Z_OFF_I), max(f_Z_OFF_I) + 0.2, step=0.1), fontsize=8)
ax1.set_xlabel("time(s)", fontsize=6)
ax1.set_ylabel("Frequency (Hz)", fontsize=6)
ax1.set_title('Frequency analisys of ' + str(sys.argv[1]) + ' DSfactor: ' 
              + str(selection_factor) + ' step: ' + str(step))
ax1.grid()

c11 = ax1.plot(np.arange(0, len(f_Z_OFF_I)), f_Z_OFF_I, label= 'Data')#graficamos los datos brutos
c12 = ax1.plot(time_list, f_model, label='fit')#graficamos la curva de ajuste de los datos en bruto
c13 = ax1.plot(t_selection, f_selection, label= 'selected data')#graficamos los datos seleccionados por el criterio
c14 = ax1.plot(t_selection, upperlim_list, label= 'upper selection limit')#graficamos el limite superior
c15 = ax1.plot(t_selection, lowerlim_list, label= 'lower selecton limit')#graficamos el limite inferior


plt.text(10, max(f_Z_OFF_I), "fit slope = " + str(slope), {'color': 'black', 'fontsize': 10})
plt.text(30, max(f_Z_OFF_I) - 0.2, str(selection_factor) + "std = " + str(selection_factor*std_delta), 
         {'color': 'black', 'fontsize': 10})
plt.text(30, max(f_Z_OFF_I)-0.3 , "r2 = " +str(r_value) , {'color': 'black', 'fontsize': 10})
ax1.legend( loc='upper right', shadow=True)


#ax1.plot(time_list2, f_selection2)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_ylim(min(f_selection), max(f_selection) + 0.2)
plt.xticks(np.arange(0, len(f_selection), step=20), fontsize=8)
plt.yticks(np.arange(min(f_selection), max(f_selection) + 0.2, step=0.1), fontsize=8)
ax2.set_xlabel("time(s)", fontsize=6)
ax2.set_ylabel("Frequency (Hz)", fontsize=6)
ax2.set_title('Selected data of ' + str(sys.argv[1]) + ' SDfactor: ' + str(selection_factor)
               + ' step: ' + str(step))
ax2.grid()

c21 = ax2.plot(t_selection, f_selection, label='Data selected')
c22 = ax2.plot(time_list2, f_model2, label = 'fit')

plt.text(10, max(f_selection), "fit slope = " + str(slope2), {'color': 'black', 'fontsize': 10})
plt.text(30, max(f_selection) - 0.2, str(selection_factor) + "std = " + str(selection_factor*std_delta), 
         {'color': 'black', 'fontsize': 10})
plt.text(30, max(f_selection)-0.3 , "r2 = " +str(r_value2) , {'color': 'black', 'fontsize': 10})
ax2.legend( loc='upper right', shadow=True)

plt.show()
