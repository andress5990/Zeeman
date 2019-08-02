import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys


import pdb

def CalDelta(vf, vi):
    
    delta = vf-vi
    return delta
    
    #if delta <= 0:
    #    return ('nv', Deltas)

def Stads(Data_list):#funcion de calculo de delta

    mean_data = 0
    std_data = 0
    
    for data in Data_list:
        data += data
        mean_data = data
    
    mean_data = mean_data/len(Data_list) 
    
    std_term = 0
    for data in Data_list:
        std_term = (data-mean_data)**2
        std_data += std_term
    
    std_data = std_data/(len(Data_list)-1)
    std_data = (std_data)**(1/2)

    return [mean_data, std_data]

def Analisys1(data_list):
    tdelta_list = []
    f_data = []
    time = []

    count = 0
    window = 2
    
    for counter in range(len(data_list)):
        if(counter < window):
            pass
        if(counter >= (window) and counter <= len(data_list)):
            delta = CalDelta(data_list[counter], data_list[counter-window])
            tdelta_list.append(delta)
    
    [mean_delta, std_delta] = Stads(tdelta_list)
            
    for delta in tdelta_list:
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

[time,f_data, mean_delta, std_delta] = Analisys1(f_Z_OFF_I)



pdb.set_trace()
