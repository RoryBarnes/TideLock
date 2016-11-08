# EDOT.PY
#
# Written by Rory Barnes
#
# Calculate time derivative of eccentricity for both the CTL and CPL models as
# a function of the ratio of frequencies. This script requires the EQTIDE 
# software package, publicly available at https://github.com/RoryBarnes/EqTide. 
# To run this script:
#
# > python edot.py
#

import numpy as np
import subprocess as subp
import matplotlib.pyplot as plt
import string

PI = np.arccos(-1)
MSUN = 1.98892e30
AUCM = 1.49598e11
RSUN = 6.955e8
BIGG = 6.67e-11
MEARTH = 5.9742e24
REARTH = 6.3781e6
PEARTH = 65.25*24*3600
SECMYR = 1e6*PEARTH
RADDEG = PI/180
YEARDAY = 365.25
CPL=0
CTL=1

semi=0.05

ecc=0.2
obl=23.5

pmin=0.3
pmax=100
dp=0.1

k2=[0 for j in range(2)]
mass=[0 for j in range(2)]
zcpl=[0 for j in range(2)]
zctl=[0 for j in range(2)]
q=[0 for j in range(2)]
tau=[0 for j in range(2)]

mass[0]=-0.1 # In Eqtide, negative for PriMass is in solar units
mass[1]=-1   # In Eqtide, negative for SecMass is in Earth units 

rearth=-1    # In Eqtide, negative for SecMass is in Earth units 

q[0]=1e6
q[1]=10

tau[0] = 0.01
tau[1] = 1000

k2[0]=0.5
k2[1]=0.3

pbin=int((pmax-pmin)/dp)

edot=[[0 for k in range(pbin)] for j in range(2)]
ratio=[0 for k in range(pbin)]

for j in range(2):
    model = j
    for p in range(pbin):
        per = pmin + p*dp
        
        file=open('tide.in','w')
        file.write("# Calculate de/dt\n")
        file.write("sSystemName           edot\n")
        if model == CPL:
            file.write("sTideModel            CPL\n")
            file.write("bDiscreteRot          1\n")
        if model == CTL:
            file.write("sTideModel           CTL\n")
        file.write("\n")
        file.write("iVerbose              5\n")
        file.write("iDigits               8\n")
        file.write("iSciNot               4\n")
        file.write("\n")
        file.write("bDoLog                1\n")
        file.write("\n")
        file.write("sUnitMass             solar\n")
        file.write("sUnitLength           AU\n")
        file.write("sUnitTime             year\n")
        file.write("sUnitAngle            degrees\n")
        file.write("\n")
        file.write("dPrimaryMass          " + repr(mass[0]) + "     # solar\n")
        file.write("sPrimaryMassRad       Baraffe15\n")
        file.write("dPrimarySpinPeriod    -30     # days\n")
        file.write("dPrimaryObliquity     0\n")
        file.write("dPrimaryRadGyra       0.5\n")
        file.write("dPrimaryK2            " + repr(k2[0]) + "\n")
        if model == CPL:
            file.write("dPrimaryQ            " + repr(q[0]) + "\n")
            if model == CTL:
                file.write("dPrimaryTau          -" + repr(tau[0]) + "\n")
        file.write("\n")
        file.write("dSecondaryMass        " + repr(mass[1]) + "\n")
        file.write("dSecondaryRadius      " + repr(rearth) + "\n")
        file.write("dSecondarySpinPeriod  -" + repr(per) + "\n")
        file.write("dSecondaryObliquity   " + repr(obl) + "\n")
        file.write("dSecondaryK2          " + repr(k2[1]) + "\n")
        file.write("dSecondaryRadGyra     0.5\n")
        if model == CPL:
            file.write("dSecondaryQ          " + repr(q[1]) + "\n")
        if model == CTL:
            file.write("dSecondaryTau        -" + repr(tau[1]) + "\n")
        file.write("\n")
        file.write("dSemi                 " + repr(semi) + "\n")
        file.write("dEcc                  " + repr(ecc) + "\n")
            
        file.close()
    
        subp.call("/Users/rory/bin/eqtide tide.in -q", shell=True)
        
        log=open("edot.log","r")
        
        found=0
        for line in log:
            words=string.split(line," ")
            if len(words) > 3:
                if words[0] == "Secondary" and words[3] == "Frequency:":
                    om2= float(words[4])
                if words[0] == "Input" and words[3] == "Motion:":
                    n = float(words[4])
            if len(words) >= 1:
                if words[0] == "de/dt:":
                    edot[j][p] = float(words[1])*1e9
                
        ratio[p] = om2/n

#### PLOT ####

plt.figure(figsize=(6.5,9), dpi=200)

plt.xlim(0,5)
plt.ylim(-0.3,0.3)
plt.tick_params(axis='both', labelsize=20)
plt.xlabel('$\Omega_2$/n',fontsize=20)
plt.ylabel('de/dt (/Gyr)',fontsize=20)
plt.plot(ratio,edot[0],linestyle='-',color='k',linewidth=2,label='CPL')
plt.plot(ratio,edot[1],linestyle='dashed',color='k',linewidth=2,label='CTL')
plt.plot([0,100],[0,0],linestyle=':',color='k')
plt.legend(loc='lower right',frameon='True')
plt.legend().get_frame().set_edgecolor('k')

plt.tight_layout()
plt.savefig('edot.ps')
