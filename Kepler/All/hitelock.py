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

def MakeBox(xmin,xmax,ymin,ymax,lc):
    plt.plot([xmin,xmax],[ymax,ymax],color=lc)
    plt.plot([xmin,xmax],[ymin,ymin],color=lc)
    plt.plot([xmin,xmin],[ymin,ymax],color=lc)
    plt.plot([xmax,xmax],[ymin,ymax],color=lc)

FontSize=18
PanelSize = [2,10]
FigSize = [2,3]

sFile='kepler.tlock.dat'
sOutFile='close100.csv'

fFile= open(sFile,'r')
fOutFile=open(sOutFile,'w')

# Get number of lines
lineWC = subp.check_output(['wc',sFile])
wordsWC = lineWC.split()
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
plt.tick_params(
    axis='x',          
    which='both',      
    bottom='on',       
    top='on',          
    labelbottom='on')  
plt.tick_params(
    axis='y',          
    which='both',      
    left='on',         
    right='on',        
    labelleft='on')    

plt.ylabel('Habitability Index', fontsize=20)
plt.xlabel('Time to Tidally Lock (Gyr)',fontsize=20)
plt.xscale('log')

for i in range(nlines):
    plt.plot(ctlearth[i],hite[i],'o',color='0.75',markersize=(3*plrad[i]))
    plt.plot(cplearth[i],hite[i],'ko',markersize=(3*plrad[i]))

plt.plot(1e6,0.85,'ko',markersize=7)
plt.plot(1e6,0.82,'o',color='0.75',markersize=7)
plt.text(1.4e6,0.8425,'CPL')
plt.text(1.4e6,0.8125,'CTL')
MakeBox(7e5,7e6,0.8,0.87,'k')

plt.plot(1e6,0.78,'ko',markersize=(3*2.5))
plt.plot(1e6,0.74,'ko',markersize=(3*1.75))
plt.plot(1e6,0.7,'ko',markersize=3)
plt.text(1.4e6,0.7725,'2.5 $R_\oplus$')
plt.text(1.4e6,0.7325,'1.75 $R_\oplus$')
plt.text(1.4e6,0.6925,'1 $R_\oplus$')
MakeBox(7e5,7e6,0.68,0.8,'k')

plt.savefig('hitelock.eps')
