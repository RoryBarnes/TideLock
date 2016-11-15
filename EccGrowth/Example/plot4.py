# PLOT4.PY
#
# Written by Rory Barnes
#
# Plot output from CPL and CTL runs of a system whose eccentricity initially
# grows. To run:
#
# > python survey.py
#
import numpy as np
import string as str
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import subprocess as subp

sCPL='edot.cpl.forward'
sCTL='edot.ctl.forward'

fCPL = open(sCPL,'r')
fCTL = open(sCTL,'r')

FontSize=15
PanelSize = [2,10]
FigSize = [2,3]

# Get number of lines
lineWC = subp.check_output(['wc',sCPL])
wordsWC = lineWC.split()
nlinesCPL=int(wordsWC[0])

#print(repr(nlinesCPL))
#exit()

lineWC = subp.check_output(['wc',sCTL])
wordsWC = lineWC.split()
nlinesCTL=int(wordsWC[0])

# Initialize columns here
timeCPL = [0 for i in range(nlinesCPL)]
SemiCPL = [0 for i in range(nlinesCPL)]
EccCPL = [0 for i in range(nlinesCPL)]
SecOblCPL = [0 for i in range(nlinesCPL)]
SecSpinCPL = [0 for i in range(nlinesCPL)]
SecPerCPL = [0 for i in range(nlinesCPL)]
MMCPL = [0 for i in range(nlinesCPL)]
FluxCPL = [0 for i in range(nlinesCPL)]
DeDtCPL = [0 for i in range(nlinesCPL)]
ratioCPL = [0 for i in range(nlinesCPL)]

timeCTL = [0 for i in range(nlinesCTL)]
SemiCTL = [0 for i in range(nlinesCTL)]
EccCTL = [0 for i in range(nlinesCTL)]
SecOblCTL = [0 for i in range(nlinesCTL)]
SecSpinCTL = [0 for i in range(nlinesCTL)]
SecPerCTL = [0 for i in range(nlinesCTL)]
MMCTL = [0 for i in range(nlinesCTL)]
FluxCTL = [0 for i in range(nlinesCTL)]
DeDtCTL = [0 for i in range(nlinesCTL)]
ratioCTL = [0 for i in range(nlinesCTL)]

j=0
for lineCPL in fCPL:
    wordsCPL = str.split(lineCPL," ")

    timeCPL[j] = float(wordsCPL[0])
    SemiCPL[j] = float(wordsCPL[1])
    EccCPL[j] = float(wordsCPL[2])
    SecOblCPL[j] = float(wordsCPL[3])
    SecSpinCPL[j] = float(wordsCPL[4])
    SecPerCPL[j] = float(wordsCPL[5])
    MMCPL[j] = float(wordsCPL[6])
    FluxCPL[j] = float(wordsCPL[7])
    DeDtCPL[j] = float(wordsCPL[8])
    ratioCPL[j] = SecSpinCPL[j]/MMCPL[j]

    j += 1

j=0
for lineCTL in fCTL:
    wordsCTL = str.split(lineCTL,' ')

    timeCTL[j] = float(wordsCTL[0])
    SemiCTL[j] = float(wordsCTL[1])
    EccCTL[j] = float(wordsCTL[2])
    SecOblCTL[j] = float(wordsCTL[3])
    SecSpinCTL[j] = float(wordsCTL[4])
    SecPerCTL[j] = float(wordsCTL[5])
    MMCTL[j] = float(wordsCTL[6])
    FluxCTL[j] = float(wordsCTL[7])
    DeDtCTL[j] = float(wordsCTL[8])
    ratioCTL[j] = SecSpinCTL[j]/MMCTL[j]

    j += 1

f, ax = plt.subplots(2,2,figsize=(8.5,11))

# First Column

ax[0,0].tick_params(axis='both', labelsize=FontSize)
ax[0,0].tick_params(
    axis='x',          
    which='both',      
    bottom='on',       
    top='on',          
    labelbottom='on')  
ax[0,0].tick_params(
    axis='y',          
    which='both',      
    left='on',         
    right='on',        
    labelleft='on')    
ax[0,0].set_ylabel('Eccentricity', fontsize=FontSize)
ax[0,0].set_xlabel('Time (Yr)',fontsize=FontSize)
ax[0,0].set_xscale('log')
ax[0,0].plot(timeCPL,EccCPL,linewidth=2,label='CPL',color='k',linestyle='-')
ax[0,0].plot(timeCTL,EccCTL,linewidth=2,label='CTL',color='k',linestyle='dashed')
ax[0,0].set_xlim([1e3,1e10])
ax[0,0].set_ylim([0,0.25])
ax[0,0].legend()
ax[0,0].legend().get_frame().set_edgecolor('k')

ax[0,1].tick_params(axis='both', labelsize=FontSize)
ax[0,1].tick_params(
    axis='x',          
    which='both',      
    bottom='on',       
    top='on',          
    labelbottom='on')  
ax[0,1].tick_params(
    axis='y',          
    which='both',      
    left='on',         
    right='on',        
    labelleft='on')    
ax[0,1].set_ylabel('$\Omega_2$/n', fontsize=FontSize)
ax[0,1].set_xlabel('Time (Yr)',fontsize=FontSize)
ax[0,1].plot(timeCPL,ratioCPL,linewidth=2,color='k',linestyle='-')
ax[0,1].plot(timeCTL,ratioCTL,linewidth=2,color='k',linestyle='dashed')
ax[0,1].set_xscale('log')
ax[0,1].set_xlim([1e3,1e10])
ax[0,1].set_ylim([0,10])

# Second Column

orbper = 12.91
x = [0 for j in range(2)]
y = [0 for j in range(2)]

x[0] = 0
x[1] = 1e10
y[0] = orbper
y[1] = orbper

ax[1,0].tick_params(axis='both', labelsize=FontSize)
ax[1,0].tick_params(
    axis='x',          
    which='both',      
    bottom='on',       
    top='on',          
    labelbottom='on')  
ax[1,0].tick_params(
    axis='y',          
    which='both',      
    left='on',         
    right='on',        
    labelleft='on')    
ax[1,0].set_ylabel('de/dt (/Gyr)', fontsize=FontSize)
ax[1,0].set_xlabel('Time (Yr)',fontsize=FontSize)
ax[1,0].set_xscale('log')
ax[1,0].plot(timeCPL,DeDtCPL,linewidth=2,color='k',linestyle='-')
ax[1,0].plot(timeCTL,DeDtCTL,linewidth=2,color='k',linestyle='dashed')
ax[1,0].set_xlim([1e3,1e10])
ax[1,0].set_ylim([-0.5,0.5])

ax[1,1].tick_params(axis='both', labelsize=FontSize)
ax[1,1].tick_params(
    axis='x',          
    which='both',      
    bottom='on',       
    top='on',          
    labelbottom='on')  
ax[1,1].tick_params(
    axis='y',          
    which='both',      
    left='on',         
    right='on',        
    labelleft='on')    
ax[1,1].set_ylabel('Rotation Period (d)', fontsize=FontSize)
ax[1,1].set_xlabel('Time (Yr)',fontsize=FontSize)
ax[1,1].plot(timeCPL,SecPerCPL,linewidth=2,color='k',linestyle='-')
ax[1,1].plot(timeCTL,SecPerCTL,linewidth=2,color='k',linestyle='dashed')
ax[1,1].plot(x,y,linewidth=2,color='k',linestyle=':')
ax[1,1].set_xscale('log')
ax[1,1].set_xlim([1e3,1e10])
ax[1,1].set_ylim([0,15])

plt.tight_layout()
plt.rcParams["figure.figsize"] = PanelSize
plt.savefig('EccGrowth.eps')
