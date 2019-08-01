import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

import pdb


#def average(deltas):

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
t_Z_OFF_I = []

f_Z_OFF_I = []
f_Z_ON = []
f_Z_OFF_F = []


average = 0
window = 4
start = 5

for df in range(len(probe)):
    for data in range(len(df1[0])):




pdb.set_trace()
    