import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import scipy.constants as const
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import glob
import os



def peaks(df,prom,H) :
    peakIndex, _ = find_peaks(df["volts"],height=H,prominence = prom)
    return peakIndex

def waveL() :
    #dirpath = "./NewRuns/deltaX/"
    dirpath = "./NewRuns/deltaX/"
    pattern = "*.csv"

    #sList = [8.38e04,1.348e5,2.08e4,1.344e05,4.18e5,6.49e5,4.86e5]
    #eList = [1.118e5,1.729e5,3.67e04,1.525e05,5.18e05,7.06e5,5.48e5]

    tot_peaks = []

    files = sorted(glob.glob(os.path.join(dirpath,pattern)))

    print(files)

    d = np.array([54e-6,56e-6,77e-6,82e-6,83e-6,68e-6,130e-6])

    for f in range(len(files)):
        df = pd.read_csv(files[f]) 
        df.columns = ["time","volts"] 
       
        peakList = peaks(df,1.5,-8)
        startInd = peakList[0]
        endInd = peakList[-1]

        tot_peaks.append(len(peakList))
     
        x_arr = np.array(df["time"].iloc[startInd:endInd])  
        y_arr = np.array(df["volts"].iloc[startInd:endInd])

        plt.plot(x_arr,y_arr)
        plt.plot(df["time"].iloc[peakList],df["volts"].iloc[peakList],"x")
        plt.savefig(str(f+1))
        plt.clf()

    wl = d/tot_peaks
    diff = abs(0.6e-6 - wl)/wl * 100
    
    finWL = (wl[0]+wl[5])/2
    finDiff = abs(0.6e-6 - finWL)/finWL * 100
    print(finWL,finDiff)
    print(tot_peaks)
    return d/tot_peaks

def PFunc(P,a):
    l = 0.4064
    k0 = 2*np.pi/0.6e-6
    T = 298
    F = ((l*k0)/(4*np.pi))*(-1 + np.sqrt((8*np.pi*a*(101325-P) + 3*const.k*T)/(3*const.k*T-4*np.pi*a*(101325-P))))
    return F

def polar():
    dirpath = "./airNew/"
    pFringe = "*F.csv"
    pPresh = "*P.csv"

    
    fileF = sorted(glob.glob(os.path.join(dirpath,pFringe)))
    fileP = sorted(glob.glob(os.path.join(dirpath,pPresh)))

    print(fileF,fileP)

    for f in range(len(fileF)):
        df = pd.read_csv(fileF[f])
        dfP = pd.read_csv(fileP[f])
        df.columns = ["time","volts"]
        dfP.columns = ["time","volts"]
        #print(dfP["volts"])
        peakList = peaks(df,1.5,1)
        sInd = peakList[0]
        eInd = peakList[-1]

        fringe = np.array(range(1,len(peakList)+1))
        presV = np.array(dfP["volts"].iloc[peakList])

        pressure = (1 + presV/10)*101325

        popt, pcov = curve_fit(PFunc, pressure, fringe,p0=[2.118e-29])

        print(popt)

        #print(f"Fringe:{f} ",fringe)
        #print(f"Pressure:{fileP[f]} ", pressure)

        


        plt.xlabel("Pressure (Pa)")
        plt.ylabel("Fringes")
        plt.plot(pressure,fringe,label="raw_data")
        plt.plot(pressure,PFunc(pressure,popt[0]),label="fit")
        plt.legend()
        plt.savefig(str(f+1))
        plt.clf()
        
    
def MS():
    dirpath = "./MS/"
    pattern = "*.csv"

    levels = [-4.8,-4.8,-3.5,-3.5] 

    tot_peaks = []

    files = sorted(glob.glob(os.path.join(dirpath,pattern)))

    print(files)

    lam = 0.6e-6

    for f in range(len(files)):
        df = pd.read_csv(files[f]) 
        df.columns = ["time","volts"] 
       
        peakList = peaks(df,1,levels[f])
        startInd = peakList[0]
        endInd = peakList[-1]

        tot_peaks.append(len(peakList))
     
        x_arr = np.array(df["time"].iloc[startInd:endInd])  
        y_arr = np.array(df["volts"].iloc[startInd:endInd])

        plt.plot(x_arr,y_arr)
        plt.plot(df["time"].iloc[peakList],df["volts"].iloc[peakList],"x")
        plt.savefig(str(f+1))
        plt.clf()

    return tot_peaks


print(MS())
