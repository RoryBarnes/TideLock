#!/usr/bin/python
import numpy as np
import subprocess as subp
import string

MSUN = 1.98892e33
AUCM = 1.49598e13
RSUN = 6.955e10
LSUN = 3.827e33
PI = 3.1415926535
SIGMA =5.67e-5
CPL=0
CTL=1

model=CPL

mp=0.1,1,10
rp=np.power(mp,0.274)
rp[0]=np.power(mp[0],0.306)

msmin=0.05
msmax=1.3
dm=0.001

amin=0.05
amax=1.8
da=0.001

per=10
obl=0
ecc=0

def HabitableZone(lum,teff,lim):
    seff = [0 for j in range(6)]
    seffsun = [0 for j in range(6)]
    aa = [0 for j in range(6)]
    b = [0 for j in range(6)]
    c = [0 for j in range(6)]
    d = [0 for j in range(6)]

    seffsun[0] = 1.7763
    seffsun[1] = 1.0385
    seffsun[2] = 1.0146
    seffsun[3] = 0.3507
    seffsun[4] = 0.2946
    seffsun[5] = 0.2484
    
    aa[0] = 1.4335e-4
    aa[1] = 1.2456e-4
    aa[2] = 8.1884e-5
    aa[3] = 5.9578e-5
    aa[4] = 4.9952e-5
    aa[5] = 4.2588e-5
    
    b[0] = 3.3954e-9
    b[1] = 1.4612e-8
    b[2] = 1.9394e-9
    b[3] = 1.6707e-9
    b[4] = 1.3893e-9
    b[5] = 1.1963e-9
    
    c[0] = -7.6364e-12
    c[1] = -7.6345e-12
    c[2] = -4.3618e-12
    c[3] = -3.0058e-12
    c[4] = -2.5331e-12
    c[5] = -2.1709e-12
    
    d[0] = -1.1950e-15
    d[1] = -1.7511E-15
    d[2] = -6.8260e-16
    d[3] = -5.1925e-16
    d[4] = -4.3896e-16
    d[5] = -3.8282e-16
 
    tstar = teff - 5700

    for j in range(6):
        seff[j] = seffsun[j] + aa[j]*tstar + b[j]*tstar**2 + c[j]*tstar**3 + d[j]*tstar**4
        lim[j] = np.sqrt(lum/seff[j])

def RadLumBoyajian12(r):
    l = -3.5822 + 6.8639*r - 7.185*r**2 + 4.5169*r**3
    return 10**l

def MassLumBaraffe15(m):
    x=np.log10(m)
    l=-0.04941 + 6.6496*x + 8.7299*x**2 + 5.2076*x**3
    return 10**l

def MassRadBaraffe15(m):
    return 0.003269 + 1.304*m - 1.312*m**2 + 1.055*m**3

def MassLumScalo07(m):
    x=np.log10(m)
    l=4.101*x**3 + 8.162*x**2 + 7.108*x + 0.065
    return 10**l

def MassLumWiki(m):
    if m < 0.43:
        l=0.23*m**2.3
    else:
        l=m**4
    return l

def MassRadWiki(m):
     return m**0.8


exe="/Users/rory/bin/eqtide"

### Automatic from here ###

abin=int((amax-amin)/da)
mbin=int((msmax-msmin)/dm)

acol=[0 for i in range(abin)]
mcol=[0 for i in range(mbin)]
t=[[[0 for i in range(abin)] for j in range(mbin)] for k in range(3)]

ttot=0
for imp in range(3):
    for im in range(mbin):
        mcol[im] = msmin + im*dm
    
        print("Stellar Mass ("+repr(imp)+","+repr(im)+"): " + repr(mcol[im]))
        for ia in range(abin):
            a = amin + ia*da
            acol[ia] = a
        
            file=open('tide.in','w')
            file.write("# Calculate timescale for tidal lock\n")
            file.write("sSystemName           tidelock\n")
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
            file.write("bDoForward            1\n")
            file.write("bVarDt                1\n")
            file.write("dForwardStopTime      1e10\n")
            file.write("dForwardOutputTime    1e9\n")
            file.write("dTimestepCoeff        0.01\n")
            file.write("dMinValue             1e-10\n")
            file.write("bHaltSecLock          1\n")
            file.write("\n")
            file.write("dPrimaryMass          " + repr(mcol[im]) + "     # solar\n")
            file.write("sPrimaryMassRad       Baraffe15\n")
            file.write("dPrimarySpinPeriod    -30     # days\n")
            file.write("dPrimaryObliquity     0\n")
            file.write("dPrimaryRadGyra       0.5\n")
            file.write("dPrimaryK2            0.5\n")
            if model == CPL:
                file.write("dPrimaryQ             1e6\n")
            if model == CTL:
                file.write("dPrimaryTau          -0.01\n")
            file.write("\n")
            file.write("dSecondaryMass        -" + repr(mp[imp]) + "\n")
            file.write("dSecondaryRadius      -" + repr(rp[imp]) + "\n")
            file.write("dSecondarySpinPeriod  -" + repr(per) + "\n")
            file.write("dSecondaryObliquity  " + repr(obl) + "\n")
            file.write("dSecondaryK2          0.5\n")
            file.write("dSecondaryRadGyra     0.5\n")
            if model == CPL:
                file.write("dSecondaryQ           12\n")
            if model == CTL:
                file.write("dSecondaryTau        -648\n")
            file.write("dSecondaryMaxLockDiff 0.1\n")
            file.write("\n")
            file.write("dSemi                 " + repr(a) + "\n")
            file.write("dEcc                  " + repr(ecc) + "\n")
            file.write("\n")
            file.write("sOutputOrder          tim semim ecce -secper -orbperiod secobl\n")
            
            file.close()
            
            subp.call("/Users/rory/bin/eqtide tide.in >& log", shell=True)
            
            log=open("log","r")
            
            found=0
            for line in log:
                words=string.split(line," ")
                if words[0] == "HALT:":
                    t[imp][im][ia]=float(words[4])/1e9
                    found=1
                    
            if found == 0:
                t[imp][im][ia]=10.1
                        
            ttot += t[imp][im][ia]


for imp in range(3):
    outname='tidelock'+repr(imp)+'.out'
    outf=open(outname,"w")
    for im in range(mbin):
        for ia in range(abin):
            outf.write(repr(t[imp][im][ia])+" ")
        outf.write("\n")

#print(t)
print('Total integrated time: '+repr(ttot)+' Gyr')

import matplotlib.pyplot as plt

#rs=mcol # From Boyajian et al. (2012)
l=[0 for i in range(mbin)]
rs=[0 for i in range(mbin)]
teff=[0 for i in range(mbin)]
rv=[0 for i in range(mbin)]   # Recent Venus
mg=[0 for i in range(mbin)]   # Moist Greenhouse
maxg=[0 for i in range(mbin)] # Maximum Greenhouse
em=[0 for i in range(mbin)]   # Early Mars
lim=[0 for j in range(6)]

#print(rs)

for im in range(mbin):
    #print(im)
    #l[im] = RadLumBoyajian12(rs[im])
    #l[im] = MassLumScalo07(mcol[im])
    #l[im] = MassLumWiki(mcol[im])
    #rs[im] = MassRadWiki(mcol[im])
    l[im] = MassLumBaraffe15(mcol[im])
    rs[im] = MassRadBaraffe15(mcol[im])
    #print(mcol[im],rs[im],l[im])
    teff[im]=((l[im]*LSUN)/(4*PI*SIGMA*(rs[im]*RSUN)**2))**0.25
    HabitableZone(l[im],teff[im],lim)
    rv[im] = lim[0]
    mg[im] = lim[2]
    maxg[im] = lim[3]
    em[im] = lim[4]
    print(mcol[im],rs[im],l[im],mg[im],maxg[im])

#### Now plot #####

plt.figure(figsize=(6.5,9), dpi=200)

fbk = {'lw':0.0, 'edgecolor':None}

plt.xlabel('Semi-Major Axis (AU)',fontsize=20)
plt.ylabel('Stellar Mass (M$_\odot$)',fontsize=20)
plt.tick_params(axis='both', labelsize=20)

xt=[0,0.25,0.5,0.75,1,1.25]
yt=[0,0.25,0.5,0.75,1,1.25]
plt.xticks(xt)
plt.yticks(yt)
plt.fill_betweenx(mcol,rv,em,facecolor='0.85', **fbk)
plt.fill_betweenx(mcol,mg,maxg,facecolor='0.75', **fbk)
#plt.plot(rv,mcol,color='yellow',linewidth=2)

ContSet0 = plt.contour(acol,mcol,t[0],3,colors='black',linestyles='dashed',
                  levels=[1,5,10],linewidths=3)
plt.clabel(ContSet0,fmt="%.0f",inline=True,fontsize=18)

ContSet1 = plt.contour(acol,mcol,t[1],3,colors='black',linestyles='solid',
                  levels=[1,5,10],linewidths=3)
plt.clabel(ContSet1,fmt="%.0f",inline=True,fontsize=18)

ContSet2 = plt.contour(acol,mcol,t[2],3,colors='black',linestyles='dotted',
                  levels=[1,5,10],linewidths=3)
plt.clabel(ContSet2,fmt="%.0f",inline=True,fontsize=18)


plt.xlim(0,1.25)
plt.ylim(0.08,1.25)

plt.tight_layout()
plt.savefig('cpl_p10o0.png')

#plt.show()
