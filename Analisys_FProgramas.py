import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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
        if(counter < window):#Condiciona a empezar cuando se tenga una cantidad de datos igual al window
            pass
        if(counter >= (window+1) and counter <= len(data_list)):
            #inicia al llevar la cantidad de valores del window, y que termine si se llega al final del array
            delta = CalDelta(data_list[counter - window], data_list[counter])#calcula el delta con un intervalo de valores igual al window
            delta_list.append(delta)#agregamos el delta a delta_list, que es temporal
            [mean_delta, std_delta] = Stads(delta_list)#calculamos del mean, y sdt con los elementos del delta_list
            
            if delta > std_delta or delta < -1*std_delta:
                #si el valor de delta se aleja de mean por mas de una std a la derecha o a la izquierda, se excluye
                pass
            if delta <= std_delta or delta >= -1*std_delta:
                #si el valor esta a menos de una std se incluye en f_data (final data)
                #ademas el count se se agrega a la lista time, (una medición por segundo) 
                time.append(count)
                f_data.append(delta)
                count +=1#se suma uno a la cuenta
                
                return [time,f_data, mean_delta, std_delta]#se devuelven las listas time, f_data, y los valores mean y std





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
