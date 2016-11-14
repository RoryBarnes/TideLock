# SURVEY.PY
#
# Written by Rory Barnes
#
# Calculate the time for a planet to tidally lock over a wide range of orbits 
# and stellar masses. This script creates output files for three different 
# planetary masses and creates the .eps file that goes into the manuscript. 
# If you have already run this script, use tlock.py to create the postscript
# and avoid rerunning all the trials again.
#
# This script requires the EQTIDE software package, publicly available at
# https://github.com/RoryBarnes/EqTide. To run this script:
#
# > python survey.py
#
# This script is specifically designed for the case of planets with initial
# spin periods of 10 days, initial obliquities of 0 degrees, and adhere to the
# CPL model.
#
import numpy as np
import subprocess as subp
import string

MSUN = 1.988416e33 	# Stellar mass in grams from Prsa et al. 2016
AUCM = 1.49598e13	# Astronomical Unit in cm recommended by the IAU
RSUN = 6.957e10     	# Stellar radius in cm from Prsa et al. 2016
LSUN = 3.828e33		# Nominal solar luminosity in cgs recommended by the IAU
PI = 3.1415926535
SIGMA = 5.6704e-5	# Stefan-Boltzmann constant in cgs units

exe="/Users/rory/bin/eqtide" 	# Location of EQTIDE
logfile="log"                   # EQTIDE log file
tidefile="tide.in"              # Name of input file for EQTIDE

# Select tidal model. Options are CPL or CTL
model='CPL'

# Base output name for plots and output files. Figures will be named
# (base + model + "." + extension, e.g. tlockCPL.png. Data files will be
# named (base + model + index + ".out")
base='tlock'

# Parameter ranges
nmp=3           # Number of planetary masses to consider
mp=0.1,1,10  	# Planetary masses in Earth masses

msmin=0.05	# Minimum stellar mass in solar units
msmax=1.3	# Maximum stellar mass in solar units
dm=0.001	# Increment in stellar mass in solar units

amin=0.05	# Minimum semi-major axis in AU
amax=1.8	# Maximum semi-major axis in AU
da=0.001	# Increment in semi-major axis in AU

# Planetary properties
plper=10	# Initial planetary rotation period in days
plobl=0		# Initial planetary obliquity in degrees
plk2=0.5	# Planet's k_2
plrg=0.5	# Planet's radius of gyration
plq=12		# Planet's tidal quality factor
pltau=640	# Planet's tidal time lag in seconds

# Stellar properties
stper=30	# Star's initial rotation period in days
stobl=0		# Star's initial obliquity in degrees
stk2=0.5	# Star's k_2
strg=0.5	# Star's radius of gyration
stq=1e6		# Star's tidal quality factor
sttau=0.01	# Star's tidal time lag in seconds

ecc=0		# Initial orbital eccentricity

# Integration Parameters
tstop=1e10      # Total time to integrate in years
tout=1e9        # Output interval in years
tcoeff=1e-2     # Timestep coefficient for dynamical timestepping
minval=1e-10    # Minimum value, see EQTIDE help 

# Plotting 
plot='eps'        # Select plot format. Options are eps, png or screen
#plot='screen'     # Select plot format. Options are eps, png or screen
xlim=[0,1.75]     # x-axis limits for plot
ylim=[0.08,1.25]  # y-axis limits for plot

# Halting condition: SecLock for tidal locking; MinEcc for e=0.01
halt='SecLock'
#halt='MinEcc'

#
####### AUTOMATIC FROM HERE #######
#

# HZ boundaries from Kopparapu et al. (2013)
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
        # Assign HZ limit to lim array
        lim[j] = np.sqrt(lum/seff[j])

# stellar mass-luminosity relation from Baraffe et al. (2015). Fit by R. Barnes.
def MassLumBaraffe15(m):
    x=np.log10(m)
    l=-0.04941 + 6.6496*x + 8.7299*x**2 + 5.2076*x**3
    return 10**l

# Stellar mass-radius relation from Baraffe et al. (2015). Fit by R. Barnes.
def MassRadBaraffe15(m):
    # Check against dBaraffe15_MassRad in util.c in the EQTIDE package
    return 0.003269 + 1.304*m - 1.312*m**2 + 1.055*m**3

# Planetary radius from Sotin et al. (2007)
def MassRadSotin07(m):
    # Scaling law is broken at 1 M_Earth
    if (m >= 1):
        return np.power(m,0.274)
    else:
        return np.power(m,0.306) 	

#
######## MAIN PROGRAM ############
#

# Calculate planetary radius in Earth radii
rp = [MassRadSotin07(mp[i]) for i in range(nmp)]

abin=int((amax-amin)/da)    # delta semi-major axis 
mbin=int((msmax-msmin)/dm)  # delta stellar mass 

acol=[(amin + i*da) for i in range(abin)]  # vector of semi-major axis values  
mcol=[(msmin + i*dm) for i in range(mbin)] # vector of stellar mass values

# Matrix of times to tidally lock. The first dimension is planetary mass,
# second dimension is stellar mass, third dimension is semi-major axis
t=[[[0 for i in range(abin)] for j in range(mbin)] for k in range(nmp)]

ttot=0      # Total integrated time

cmd = (exe+" "+tidefile+" >& "+logfile) # Command to run EQTIDE

# Loop over planetary masses, stellar masses and semi-major axes and
# calculate time to tidally lock.
for imp in range(nmp):
    for im in range(mbin):

        print("Stellar Mass ("+repr(imp)+","+repr(im)+"): " + repr(mcol[im]))
        for ia in range(abin):
            a = acol[ia]
            
            # Write input file for eqtide
            file=open('tide.in','w')
            file.write("# Calculate timescale for tidal lock\n")
            file.write("sSystemName           tidelock\n")
            file.write("bDiscreteRot          1\n")
            file.write("sTideModel            "+model+"\n")
            file.write("\n")
            # Don't change verbosity as EQTIDE's STDOUT is scanned later!
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
            file.write("dForwardStopTime      "+repr(tstop)+"\n")
            file.write("dForwardOutputTime    "+repr(tout)+"\n")
            file.write("dTimestepCoeff        "+repr(tcoeff)+"\n")
            file.write("dMinValue             "+repr(minval)+"\n")
            if (halt == "SecLock"):
                file.write("bHaltSecLock          1\n")
            elif (halt == "MinEcc"):
                file.write("dHaltMinEcc          0.01\n")
            else:
                print("ERROR: Unknown halt condition: "+halt+"!\n")
                exit();
            file.write("\n")
            file.write("dPrimaryMass          " + repr(mcol[im]) + "     # solar\n")
            file.write("sPrimaryMassRad       Baraffe15\n")
            file.write("dPrimarySpinPeriod    -"+repr(stper)+"     # days\n")
            file.write("dPrimaryObliquity     "+repr(stobl)+"\n")
            file.write("dPrimaryRadGyra       "+repr(strg)+"\n")
            file.write("dPrimaryK2            "+repr(stk2)+"\n")
            file.write("dPrimaryQ             "+repr(stq)+"\n")
            file.write("dPrimaryTau          -"+repr(sttau)+"\n")
            file.write("\n")
            file.write("dSecondaryMass        -" + repr(mp[imp]) + "\n")
            file.write("dSecondaryRadius      -" + repr(rp[imp]) + "\n")
            file.write("dSecondarySpinPeriod  -" + repr(plper) + "\n")
            file.write("dSecondaryObliquity   " + repr(plobl) + "\n")
            file.write("dSecondaryK2          "+repr(plk2)+"\n")
            file.write("dSecondaryRadGyra     "+repr(plrg)+"\n")
            file.write("dSecondaryQ           "+repr(plq)+"\n")
            file.write("dSecondaryTau        -"+repr(pltau)+"\n")
            file.write("dSecondaryMaxLockDiff 0.1\n")
            file.write("\n")
            file.write("dSemi                 " + repr(a) + "\n")
            file.write("dEcc                  " + repr(ecc) + "\n")
            file.write("\n")
            file.write("sOutputOrder          tim semim ecce -secper -orbperiod secobl\n")
            
            file.close()
            
            # Run eqtide, dump output into file log
            subp.call(cmd, shell=True)
            
            log=open(logfile,"r")
            
            # Search for time to tidally lock
            found=0
            for line in log:
                words=string.split(line," ")
                if words[0] == "HALT:":
                    t[imp][im][ia]=float(words[4])/1e9
                    found=1

            # If the code did not halt, then the planet did not lock
            if found == 0:
                # Add 0.1 Gyr to locking timescale to produce prettier plots
                t[imp][im][ia]=tstop+0.1 
                        
            ttot += t[imp][im][ia]

# Dump data into output files
for imp in range(nmp):
    outname=base+model+repr(imp)+'.out'
    outf=open(outname,"w")
    for im in range(mbin):
        for ia in range(abin):
            outf.write(repr(t[imp][im][ia])+" ")
        outf.write("\n")

print('Total integrated time: '+repr(ttot)+' Gyr')

# Calculate HZ boundaries
l=[0 for i in range(mbin)]    # Stellar luminosity
rs=[0 for i in range(mbin)]   # Stellar radius
teff=[0 for i in range(mbin)] # Stellar effective temperature
rv=[0 for i in range(mbin)]   # Recent Venus
mg=[0 for i in range(mbin)]   # Moist Greenhouse
maxg=[0 for i in range(mbin)] # Maximum Greenhouse
em=[0 for i in range(mbin)]   # Early Mars
lim=[0 for j in range(6)]     # HZ limits

for im in range(mbin):
    l[im] = MassLumBaraffe15(mcol[im])
    rs[im] = MassRadBaraffe15(mcol[im])
    teff[im]=((l[im]*LSUN)/(4*PI*SIGMA*(rs[im]*RSUN)**2))**0.25
    HabitableZone(l[im],teff[im],lim)
    rv[im] = lim[0]
    mg[im] = lim[2]
    maxg[im] = lim[3]
    em[im] = lim[4]

# 
######### PLOT ###########
#

import matplotlib.pyplot as plt

plt.figure(figsize=(6.5,9), dpi=200)

fbk = {'lw':0.0, 'edgecolor':None}

plt.xlabel('Semi-Major Axis (AU)',fontsize=20)
plt.ylabel('Stellar Mass (M$_\odot$)',fontsize=20)

plt.fill_betweenx(mcol,rv,em,facecolor='0.85', **fbk)
plt.fill_betweenx(mcol,mg,maxg,facecolor='0.75', **fbk)

ContSet0 = plt.contour(acol,mcol,t[0],3,colors='black',linestyles='dashed',
                  levels=[1,5,10],linewidths=3)
plt.clabel(ContSet0,fmt="%.0f",inline=True,fontsize=18)

ContSet1 = plt.contour(acol,mcol,t[1],3,colors='black',linestyles='solid',
                  levels=[1,5,10],linewidths=3)
plt.clabel(ContSet1,fmt="%.0f",inline=True,fontsize=18)

ContSet2 = plt.contour(acol,mcol,t[2],3,colors='black',linestyles='dotted',
                  levels=[1,5,10],linewidths=3)
plt.clabel(ContSet2,fmt="%.0f",inline=True,fontsize=18)

xt=[0,0.25,0.5,0.75,1,1.25,1.5]
yt=[0,0.25,0.5,0.75,1,1.25,1.5]
plt.xticks(xt)
plt.yticks(yt)
plt.xlim(xlim)
plt.ylim(ylim)
plt.tick_params(axis='both',labelsize=20)
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

if (plot == 'eps'):
    plt.tight_layout()
    plotfile=(base+model+"."+plot)
    plt.savefig(plotfile)
elif (plot == 'png'):
    plt.tight_layout()
    plotfile=(base+model+"."+plot)
    plt.savefig(plotfile)
elif (plot == 'screen'):
    plt.show()
else:
    print("ERROR: unknown plot type: "+plot+". Options are ps, png, or screen.\n")
