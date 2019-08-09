import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import statistics


import pdb


def CalDelta(vf, vi):

    delta = vf - vi
    return delta

    # if delta <= 0:
    #    return ('nv', Deltas)


def Stads(Data_list):  # funcion de calculo de delta

    mean_data = 0

    for data in Data_list:
        data += data
        mean_data = data

    mean_data = mean_data / len(Data_list)

    std_data = statistics.stdev(Data_list)

    return [mean_data, std_data]


def Analisys1(data_list, window, std_factor):
    temp_delta_list = []  # lista temporal para calculo de los Deltas
    final_data = []  # Datos finales de los deltas frecuencia
    time = []

    count = 0  # Lleva un conteo para cada delta
    # salto entre valores para tomar el dental

    for counter in range(len(data_list)):
        # Recorremos la lista data list, por posicion
        if counter < window:  # No empezamos si no hasta recorrer tantos valores como el window

            pass  # Si la condicion no se cumple, pasamos

        if counter >= window and counter <= len(data_list):
            # recorremos data list por posicion y realizamos la accion segun
            # hasta terminar la lista

            # Calculamos el delta
            delta = CalDelta(data_list[counter], data_list[counter - window])
            # Agregamos el valor de delta a tdelta_list
            temp_delta_list.append(delta)

    # hacemos la estadistica para  obtener la DS y el Mean
    [mean_delta, std_delta] = Stads(temp_delta_list)

    # Recorremos nuevamente la lista de deltas y seleccionamos segun el
    # criterio de la DS y el mean
    for delta in temp_delta_list:
        if delta > std_factor*std_delta or delta < -std_factor * std_delta:
            pass

        if delta <= std_factor*std_delta or delta >= -std_factor * std_delta:
            time.append(count)
            final_data.append(delta)
            count += 1

    return [time, final_data, mean_delta, std_delta]

def Analisys2(data_list, std_delta, window, std_factor):
    final_data = []
    time = []
    count = 0
    
    for counter in range(len(data_list)):
        if counter < window:
            pass
        
        if counter >= window and counter <= len(data_list):
            delta = CalDelta(data_list[counter], data_list[counter - window])
            
            if delta > std_factor*std_delta or delta < -std_factor * std_delta:
                pass
            if delta < std_factor*std_delta or delta > -std_factor* std_delta:
                time.append(count)
                final_data.append(data_list[counter])
                count += 1
                
    return [time, final_data]
        


file_name = str(sys.argv[1])

window = 5
std_factor = 1/1000

reader = pd.ExcelFile(file_name)
sheetlist = reader.sheet_names

df1 = pd.read_excel(file_name, sheet_name=sheetlist[2], header=None, usecols="A, B")
df1_headers = df1.head(0)
df2 = pd.read_excel(file_name, sheet_name=sheetlist[3], header=None, usecols="A, B")
df2_headers = df2.head(0)
df3 = pd.read_excel(file_name, sheet_name=sheetlist[4], header=None, usecols="A, B")
df3_headers = df2.head(0)

probe = [df1, df2, df3]

t_Z_OFF_I = []
t_Z_ON = []
t_Z_OFF_F = []

f_Z_OFF_I = []
f_Z_ON = []
f_Z_OFF_F = []


#for df in range(len(probe)):
for data in range(len(df1[0])):
    t_Z_OFF_I.append(df1[0][data])
    f_Z_OFF_I.append(df1[1][data])

for data in range(len(df2[0])):
    t_Z_ON.append(df2[0][data])
    f_Z_ON.append(df2[1][data])

for data in range(len(df3[0])):
    t_Z_OFF_F.append(df3[0][data])
    f_Z_OFF_F.append(df3[1][data])


#Realizamos el analisis de deltas
[time1, delta_data, mean_delta, std_delta] = Analisys1(f_Z_ON, window, std_factor)
#Realizamos la seleccion
[time2, frequency_data] = Analisys2(f_Z_ON, std_delta, window, std_factor)

#pdb.set_trace()

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.set_ylim(min(delta_data), max(delta_data) + 0.2)
# ax1.set_xlim(min(time), max(time))
plt.xticks(np.arange(min(time1), max(time1), step=60), fontsize=8)
plt.yticks(np.arange(min(delta_data), max(delta_data) + 0.2, step=0.1), fontsize=8)
ax1.set_xlabel("time(s)", fontsize=6)
ax1.set_ylabel("Delta Frequency (Hz)", fontsize=6)
ax1.grid()

ax1.plot(time1, delta_data)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_ylim(min(frequency_data), max(frequency_data) + 0.2)
plt.xticks(np.arange(min(time2), max(time2), step=60), fontsize=8)
plt.yticks(np.arange(min(frequency_data), max(frequency_data) + 0.2, step=0.1), fontsize=8)
ax2.set_xlabel("time(s)", fontsize=6)
ax2.set_ylabel("Frequency (Hz)", fontsize=6)
ax2.grid()

ax2.plot(time2, frequency_data)

plt.show()
#pdb.set_trace()
