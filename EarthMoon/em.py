# EM.PY
#
# Plot the history of the Earth-Moon orbit for different assumptions. The
# input files for this script were generated with EQTIDE and the input file
# earthmoon.in. To run:
#
# > python em.oy

import numpy as np
import string as str
import matplotlib.pyplot as plt
import matplotlib.lines as lines

def AddCurve(infile,ls,col,lbl,nlines):

    infile=open(infile,"r")

    t=[0 for i in range(nlines)]
    a=[0 for i in range(nlines)]
    e=[0 for i in range(nlines)]
    pper=[0 for i in range(nlines)]
    pobl=[0 for i in range(nlines)]
    sper=[0 for i in range(nlines)]
    sobl=[0 for i in range(nlines)]
    orbper=[0 for i in range(nlines)]
    
    j=0
    for line in infile:
        words=str.split(line," ")
        t[j]=float(words[0])
        a[j]=float(words[1])
        e[j]=float(words[2])
        pper[j]=float(words[3])
        pobl[j]=float(words[4])
        sper[j]=float(words[5])
        sobl[j]=float(words[5])
        orbper[j]=float(words[5])
        
        j += 1

    plt.plot(t,a, linestyle=ls, color=col, linewidth=2, label=lbl)
        

plt.figure(figsize=(6.5,8), dpi=200)

plt.xlim(-7.5,0)
plt.ylim(0,75)
plt.tick_params(axis='both', labelsize=20)
plt.ylabel(r'Semi-major Axis (R$_\oplus$)', fontsize=20)
plt.xlabel('Time (Gyr)',fontsize=20)

AddCurve('earthmoon.q12','-','k','Q = 12, e = 0',161)
AddCurve('earthmoon.q34','-','b','Q = 34, e = 0',452)
AddCurve('orbit.q12','-','g','Q = 12, e = 0.06',182)
AddCurve('orbit.q34','-','c','Q = 34, e = 0.06',485)

AddCurve('earthmoon.tau640',':','k',r'$\tau$ = 640s, e = 0',90)
AddCurve('earthmoon.tau125',':','b',r'$\tau$ = 125s, e = 0',456)
AddCurve('orbit.tau640',':','g',r'$\tau$ = 640s, e = 0.06',95)
AddCurve('orbit.tau125',':','c',r'$\tau$ = 125s, e = 0.06',481)

plt.legend(loc='upper left')

plt.tight_layout()

plt.savefig('earthmoon.eps')

