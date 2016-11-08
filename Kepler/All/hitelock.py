# HITELOCK.PY
#
# This file creates Fig. 5 in the manuscript. This file expects that the 
# sortkoi.pl script has already been run. To run:
#
# > python hitelock.py
#
import numpy as np
import string as str
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import subprocess as subp

FontSize=18
PanelSize = [2,10]
FigSize = [2,3]

sFile='kepler.tlock.dat'
fFile= open(sFile,'r')

# Get number of lines
lineWC = subp.check_output(['wc',sFile])
wordsWC = lineWC.split()
# print wordsWC[0]+" "+wordsWC[1]
nlines=int(wordsWC[0])

# Read infile
name = ['' for i in range(nlines)]
strad = [0 for i in range(nlines)]
stmass = [0 for i in range(nlines)]
per = [0 for i in range(nlines)]
plrad = [0 for i in range(nlines)]
plmass = [0 for i in range(nlines)]
semi = [0 for i in range(nlines)]
hite = [0 for i in range(nlines)]
cplshort = [0 for i in range(nlines)]
cplearth = [0 for i in range(nlines)]
cpllong = [0 for i in range(nlines)]
ctlshort = [0 for i in range(nlines)]
ctlearth = [0 for i in range(nlines)]
ctllong = [0 for i in range(nlines)]

# Read in Data
for i in range(nlines):
    #print i
    line=fFile.readline().split()
    name[i] = line[0]
    strad[i] = float(line[1])
    stmass[i] = float(line[2])
    per[i] = float(line[3])
    plrad[i] = float(line[4])
    plmass[i] = float(line[5])
    semi[i] = float(line[6])
    hite[i] = float(line[7])
    cplshort[i] = float(line[8])*1e9
    cplearth[i] = float(line[9])*1e9
    cpllong[i] = float(line[10])*1e9
    ctlshort[i] = float(line[11])*1e9
    ctlearth[i] = float(line[12])*1e9
    ctllong[i] = float(line[13])*1e9

plt.figure(figsize=(6.5,9), dpi=200)

plt.xlim(5e5,2e10)
plt.ylim(0,1)
plt.tick_params(axis='both', labelsize=15)
plt.ylabel('Habitability Index', fontsize=20)
plt.xlabel('Time to Tidally Lock (Gyr)',fontsize=20)
plt.xscale('log')

for i in range(nlines):
    plt.plot(ctlearth[i],hite[i],'o',color='0.75',markersize=(3*plrad[i]))
    plt.plot(cplearth[i],hite[i],'ko',markersize=(3*plrad[i]))
    
plt.savefig('hitelock.eps')
