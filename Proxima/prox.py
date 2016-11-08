# PROX.PY
#
# Plot the evolution of Proxima b from previously generated forward files.
# To run:
#
# > python prox.py
#
import numpy as np
import string as str
import matplotlib.pyplot as plt
import matplotlib.lines as lines

f, ax = plt.subplots(3,1,figsize=(12,15))

def MakeBox(xmin,xmax,ymin,ymax,lc):
    ax[0].plot([xmin,xmax],[ymax,ymax],color=lc)
    ax[0].plot([xmin,xmax],[ymin,ymin],color=lc)
    ax[0].plot([xmin,xmin],[ymin,ymax],color=lc)
    ax[0].plot([xmax,xmax],[ymin,ymax],color=lc)

def AddCurve(infile,ls,col,lbl):

    infile=open(infile,"r")

    t=[0 for i in range(7000001)]
    a=[0 for i in range(7000001)]
    e=[0 for i in range(7000001)]
    p=[0 for i in range(7000001)]
    o=[0 for i in range(7000001)]
    f=[0 for i in range(7000001)]
    
    j=0
    for line in infile:
        words=str.split(line," ")
        t[j]=float(words[0])
        a[j]=float(words[1])
        e[j]=float(words[2])
        p[j]=float(words[3])
        o[j]=float(words[4])
        f[j]=float(words[5])
        
        j += 1

    if ls == '-':
        ax[0].plot(t,p, linestyle=ls, color=col, linewidth=2, label=lbl)
        ax[1].plot(t,e, linestyle=ls, color=col, linewidth=2, label=lbl)
        ax[2].plot(t,a, linestyle=ls, color=col, linewidth=2, label=lbl)
    else:
        ax[0].plot(t,p, linestyle=ls, color=col, linewidth=2)
        ax[1].plot(t,e, linestyle=ls, color=col, linewidth=2)
        ax[2].plot(t,a, linestyle=ls, color=col, linewidth=2)
        
#### Plot ####

plt.tick_params(axis='both', labelsize=15)
plt.xlabel('Apparent J Magnitude', fontsize=20)
plt.ylabel('Max. Time to Tidally Lock (Years)',fontsize=20)

for j in range(3):
    ax[j].set_xscale('log')
    ax[j].set_xlim(1e3,7e9)
    ax[j].tick_params(axis='both', labelsize=20)
    ax[j].set_xlabel('Time (Year)',fontsize=20)

ax[0].set_ylim(1,25)
ax[0].set_ylabel('Rotation Period (d)', fontsize=20)

ax[1].set_ylim(-0.01,0.42)
ax[1].set_ylabel('Eccentricity', fontsize=20)

ax[2].set_ylim(0.04,0.075)
ax[2].set_ylabel('Semi-major Axis (AU)', fontsize=20)

AddCurve('proximabCTL0.forward',':','k','e=0')
AddCurve('proximabCTL0.1.forward',':','b','e=0.1')
AddCurve('proximabCTL0.2.forward',':','g','e=0.2')
AddCurve('proximabCTL0.3.forward',':','c','e=0.3')
AddCurve('proximabCTL0.4.forward',':','m','e=0.4')

AddCurve('proximabCPL0.forward','-','k','e=0')
AddCurve('proximabCPL0.1.forward','-','b','e=0.1')
AddCurve('proximabCPL0.2.forward','-','g','e=0.2')
AddCurve('proximabCPL0.3.forward','-','c','e=0.3')
AddCurve('proximabCPL0.4.forward','-','m','e=0.4')

ax[0].legend(loc='upper left')

ax[0].plot([3e4,1e5],[22,22],color='k',lw=2)
ax[0].plot([3e4,1e5],[19,19],ls=':',color='k',lw=2)

ax[0].text(1.3e5,21.5,'CPL',fontsize=20)
ax[0].text(1.3e5,18.5,'CTL',fontsize=20)

MakeBox(2.2e4,5e5,16.5,24.25,'k')

plt.savefig('proximab.eps')

