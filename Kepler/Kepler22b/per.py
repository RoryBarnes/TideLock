# PER.PY
#
# Create plot of the evolution of Kepler-22 b's rotational evolution. The 
# input and data files are provided. To run:
#
# > python per.py
#
import numpy as np
import string as str
import matplotlib.pyplot as plt
import matplotlib.lines as lines

def AddCurve(infile,ls,col,lbl):

    infile=open(infile,"r")

    t=[0 for i in range(15001)]
    a=[0 for i in range(15001)]
    e=[0 for i in range(15001)]
    p=[0 for i in range(15001)]
    o=[0 for i in range(15001)]
    f=[0 for i in range(15001)]
    
    j=0
    for line in infile:
        words=str.split(line," ")
        t[j]=float(words[0])/1e9
        a[j]=float(words[1])
        e[j]=float(words[2])
        p[j]=float(words[3])
        o[j]=float(words[4])
        f[j]=float(words[5])
        
        j += 1

    if ls == '-':
        plt.plot(t,p, linestyle=ls, color=col, linewidth=2, label=lbl)
    else:
        plt.plot(t,p, linestyle=ls, color=col, linewidth=2)
        

plt.figure(figsize=(6.5,9), dpi=200)

plt.yscale('log')
plt.xlim(0,13.7)
plt.ylim(1,365)
plt.tick_params(axis='both', labelsize=20)
plt.ylabel('Rotation Period (d)', fontsize=20)
plt.xlabel('Time (Gyr)',fontsize=20)

AddCurve('kepler22bCPL0.forward','-','k','e=0')
AddCurve('kepler22bCPL0.1.forward','-','b','e=0.1')
AddCurve('kepler22bCPL0.2.forward','-','g','e=0.2')
AddCurve('kepler22bCPL0.3.forward','-','c','e=0.3')
AddCurve('kepler22bCPL0.4.forward','-','m','e=0.4')

AddCurve('kepler22bCTL0.forward',':','k','e=0')
AddCurve('kepler22bCTL0.1.forward',':','b','e=0.1')
AddCurve('kepler22bCTL0.2.forward',':','g','e=0.2')
AddCurve('kepler22bCTL0.3.forward',':','c','e=0.3')
AddCurve('kepler22bCTL0.4.forward',':','m','e=0.4')

plt.legend(loc='upper left')

plt.text(10.8,150,'CPL',fontsize=20)
plt.text(10.8,2,'CTL',fontsize=20)

plt.tight_layout()
plt.savefig('kepler22b.tidelock.eps')


