import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import glob
import os



def peaks(df) :
    peakIndex, _ = find_peaks(df["volts"],height=-8,prominence = 1.5)
    return peakIndex


dirpath = "./NewRuns/deltaX/"
pattern = "*.csv"

#sList = [8.38e04,1.348e5,2.08e4,1.344e05,4.18e5,6.49e5,4.86e5]
#eList = [1.118e5,1.729e5,3.67e04,1.525e05,5.18e05,7.06e5,5.48e5]

tot_peaks = []

files = sorted(glob.glob(os.path.join(dirpath,pattern)))

for f in range(len(files)):
    df = pd.read_csv(files[f]) 
    df.columns = ["time","volts"] 
   
    peakList = peaks(df)
    startInd = peakList[0]
    endInd = peakList[-1]

    tot_peaks.append(len(peakList))
 
    x_arr = np.array(df["time"].iloc[startInd:endInd])  
    y_arr = np.array(df["volts"].iloc[startInd:endInd])

    plt.plot(x_arr,y_arr)
    plt.plot(df["time"].iloc[peakList],df["volts"].iloc[peakList],"x")
    plt.savefig(str(f+1))
    plt.clf()

print(tot_peaks)

