import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

from statistics import mean, stdev

import pdb

def CalDelta(vi, vf):
    
    delta = vi-vf
    if delta >= 0:
        return delta
    
    #if delta <= 0:
    #    return ('nv', Deltas)

def Stads(window_list):#funcion de calculo de delta

    mean_data = mean(window_list)
    std_data = stdev(window_list)

    return [mean_data, std_data]

def Analisys1(data_list):#funcion de analisis
    delta_list = []#Esta lista acumula temporalemente los datos de frecuencia para calcular la ds
    f_data = []#son los datos dinales de frecuencia
    time = []#Acumula el dato de tiempo

    count = 0#Coun lleva la cuenta, define el tiempo para la selección de datos
    window = 4#el window es la magntud del step para calcular el delta
    for counter in range(len(data_list)):
        if(counter < window):#Condiciona a haber pasado 
            pass
        if(counter >= (window+1) and counter <= len(data_list)):
            delta = CalDelta(data_list[counter - window], data_list[counter])
            delta_list.append(delta)
            [mean_delta, std_delta] = Stads(delta_list)
            
            if delta > std_delta or delta < -1*std_delta:
                pass
            if delta <= std_delta or delta >= -1*std_delta:
                time.append(count)
                f_data.append(delta)
                count +=1
                
                return [time,f_data, mean_delta, std_delta]





file_name = str(sys.argv[1])

reader = pd.ExcelFile(file_name)
sheetlist = reader.sheet_names

df1 = pd.read_excel(file_name, sheet_name=sheetlist[2], header=None, usecols= "A, B")
df1_headers = df1.head(0)
df2 = pd.read_excel(file_name, sheet_name=sheetlist[3], header=None,usecols= "A, B")
df2_headers = df2.head(0)
df3 = pd.read_excel(file_name, sheet_name=sheetlist[4], header=None ,usecols= "A, B")
df3_headers = df2.head(0)

probe = [df1, df2, df3]

t_Z_OFF_I = []
t_Z_ON = []
t_Z_OFF_F = []

f_Z_OFF_I = []
f_Z_ON = []
f_Z_OFF_F = []


for df in range(len(probe)):
    for data in range(len(df1[0])):
        t_Z_OFF_I.append(df1[0][data])
        f_Z_OFF_I.append(df1[1][data])

    for data in range(len(df2[0])):
        t_Z_ON.append(df2[0][data])
        f_Z_ON.append(df2[1][data])

    for data in range(len(df3[0])):
        t_Z_OFF_F.append(df3[0][data])
        f_Z_OFF_F.append(df3[1][data])





pdb.set_trace()
