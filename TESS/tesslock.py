# TESSLOCK.PY
#
# This script calculates tidal locking times and HITE values for the 
# potentially habitable predicted in Sullivan et al. (2015). This script
# relies on the EQTIDE and HITE software packages which are publicly
# available at https://github.com/RoryBarnes. To run:
#
# python tesslock.py
#
import numpy as np
import string as str
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import subprocess as subp

# cgs
BIGG=6.67428e-8
PI=np.arccos(-1)
AUCM=1.49598e13
RSUN=6.957e10
REARTH=6.3781e8
DAYSEC=24*3600
MSUN=1.988416e33
MEARTH=5.972186e27

eqtide="/Users/rory/bin/eqtide"  # Path to eqtide
hite_exe="/Users/rory/bin/hite"  # Path to hite

def GetNumLines(sFile):
    lineWC = subp.check_output(['wc',sFile])
    wordsWC = lineWC.split()

    return int(wordsWC[0])

def LockTime(name,model,stmass,strad,plmass,plrad,plper,plobl,q,tau,semi):
    fTide = open('tide.in','w')

    fTide.write("# Calculate timescale for circularization\n")
    fTide.write("sSystemName           "+repr(name)+"\n")
    fTide.write("sTideModel            "+model+"\n")
    fTide.write("bDiscreteRot          1\n")
    fTide.write("\n")
    fTide.write("iVerbose              5\n")
    fTide.write("iDigits               8\n")
    fTide.write("iSciNot               4\n")
    fTide.write("\n")
    fTide.write("bDoLog                1\n")
    fTide.write("\n")
    fTide.write("sUnitMass             solar\n")
    fTide.write("sUnitLength           AU\n")
    fTide.write("sUnitTime             year\n")
    fTide.write("sUnitAngle            degrees\n")
    fTide.write("\n")
    fTide.write("bDoForward            1\n")
    fTide.write("bVarDt                1\n")
    fTide.write("dForwardStopTime      1.5e10\n")
    fTide.write("dForwardOutputTime    1e9\n")
    fTide.write("dTimestepCoeff        0.01\n")
    fTide.write("dMinValue             1e-10\n")
    fTide.write("bHaltSecLock          1\n")
    fTide.write("\n")
    fTide.write("dPrimaryMass          "+repr(stmass/MSUN)+"\n")
    fTide.write("dPrimaryRadius        -"+repr(strad)+"\n")
    fTide.write("dPrimarySpinPeriod    -30\n")
    fTide.write("dPrimaryObliquity     0\n")
    fTide.write("dPrimaryRadGyra       0.5\n")
    fTide.write("dPrimaryK2            0.5\n")
    fTide.write("dPrimaryQ             1e6\n")
    fTide.write("dPrimaryTau           -0.01\n")
    fTide.write("\n")
    fTide.write("dSecondaryMass        -"+repr(plmass)+"\n")
    fTide.write("dSecondaryRadius      -"+repr(plrad)+"\n")
    fTide.write("dSecondarySpinPeriod  -"+repr(plper)+"\n")
    fTide.write("dSecondaryObliquity   "+repr(plobl)+"\n")
    fTide.write("dSecondaryK2          0.3\n")
    fTide.write("dSecondaryRadGyra     0.5\n")
    fTide.write("dSecondaryQ           "+repr(q)+"\n")
    fTide.write("dSecondaryTau         -"+repr(tau)+"\n")
    fTide.write("dSecondaryMaxLockDiff 0.1\n")
    fTide.write("\n")
    fTide.write("dSemi                 "+repr(semi)+"\n")
    fTide.write("dEcc                  0\n")
    fTide.write("\n")
    fTide.write("sOutputOrder          tim semim ecce -secper -orbperiod secobl\n")

    fTide.close()
    
    cmd = eqtide+" tide.in >& log"
    subp.call(cmd, shell=True)

    sTideOut='log'
    fTideOut = open(sTideOut,'r')
    nlines = GetNumLines(sTideOut)

    tlock=15; # If no halt found, tlock > 15 Gyr
    for i in range(nlines):
        words = fTideOut.readline().split()
        if (words[0] == "HALT:"):
            if (words[1] == "Secondary") :
                tlock = float(words[4])/1e6

    return tlock;

def MakeBox(xmin,xmax,ymin,ymax,lc):
    plt.plot([xmin,xmax],[ymax,ymax],color=lc)
    plt.plot([xmin,xmax],[ymin,ymin],color=lc)
    plt.plot([xmin,xmin],[ymin,ymax],color=lc)
    plt.plot([xmax,xmax],[ymin,ymax],color=lc)

######## Main Program #########

plt.figure(figsize=(8,9), dpi=200)
plt.xlim(6,12)
plt.ylim(1e4,2e10)
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
plt.xlabel('Apparent J Magnitude', fontsize=20)
plt.ylabel('Max Time to Tidally Lock (Years)',fontsize=20)
plt.yscale('log')

sFile='planets.dat'
sOutFileS='tess.tlock.single.dat'
sTexFileS='tess.tlock.single.tex'
sOutFileM='tess.tlock.multi.dat'
sTexFileM='tess.tlock.multi.tex'

fFile= open(sFile,'r')
fOutFileS=open(sOutFileS,'w')
fTexFileS=open(sTexFileS,'w')
fOutFileM=open(sOutFileM,'w')
fTexFileM=open(sTexFileM,'w')

# Get number of lines
nlines = GetNumLines(sFile)

#print(nlines)

# File columns
num = [(i+1) for i in range(nlines)]
rpl = [0 for i in range(nlines)]
per = [0 for i in range(nlines)]
instell = [0 for i in range(nlines)]
rv = [0 for i in range(nlines)]
rstar = [0 for i in range(nlines)]
teff = [0 for i in range(nlines)]
jmag = [0 for i in range(nlines)]
snr = [0 for i in range(nlines)]
npl = [0 for i in range(nlines)]

# Derived quantities
semi = [0 for i in range(nlines)]
mpl = [0 for i in range(nlines)]
mstar = [0 for i in range(nlines)]
lum = [0 for i in range(nlines)]
logg = [0 for i in range(nlines)]
depth = [0 for i in range(nlines)]
dur = [0 for i in range(nlines)]

# I only plot cpllong, so it is the only array, but the others are here
# if useful
#
#hite = [0 for i in range(nlines)]
#cplshort = [0 for i in range(nlines)]
#cplearth = [0 for i in range(nlines)]
cpllong = [0 for i in range(nlines)]
#ctlshort = [0 for i in range(nlines)]
#ctlearth = [0 for i in range(nlines)]
#ctllong = [0 for i in range(nlines)]

# Read in data and calculate derived quantities 
for i in range(nlines):
    line=fFile.readline().split()
    rpl[i] = float(line[0])
    per[i] = float(line[1])
    instell[i] = float(line[2])
    rv[i] = float(line[3])
    rstar[i] = float(line[4])
    teff[i] = float(line[5])
    jmag[i] = float(line[6])
    snr[i] = float(line[7])
    npl[i] = int(line[8])

    # If the planet is isolated and phabitable, compute quantities
    if (rpl[i] < 2.5 and instell[i] < 5):
        print("Planet: "+repr(i))
        semi[i] = np.sqrt(1./instell[i])*rstar[i]*(teff[i]/5777)**2
        mstar[i] = 4*PI**2/(BIGG*(per[i]*DAYSEC)**2) * (semi[i]*AUCM)**3
        logg[i] = np.log10(BIGG*mstar[i]/((rstar[i]*RSUN)**2))
        depth[i] = (rpl[i]*REARTH)**2/((rstar[i]*RSUN)**2)*1e6 # ppm
        dur[i] = (rstar[i]*RSUN)*(per[i]*24)/(PI*semi[i]*AUCM) # hr

        if (rpl[i] < 1):
            mpl[i] = rpl[i]**3.268
        else:
            mpl[i] = rpl[i]**3.65

        # Get HITE
        fHiteIn = open('hite.in','w')
        fHiteIn.write('NumPlanets\t1\n')
        fHiteIn.write('StellarLogG\t'+repr(logg[i])+'\n')
        fHiteIn.write('StellarRadius\t'+repr(rstar[i])+'\n')
        fHiteIn.write('StellarTemp\t'+repr(teff[i])+'\n')
        fHiteIn.write('\n')
        fHiteIn.write('BodyPos\t\t1\n')
        fHiteIn.write('TransitDepth\t'+repr(depth[i])+'\n')
        fHiteIn.write('Period\t\t'+repr(per[i])+'\n')
        fHiteIn.write('Duration\t'+repr(dur[i])+'\n')
        fHiteIn.write('ImpactParam\t0.0\n')

        fHiteIn.close()

        cmd=hite_exe+" hite.in"
        subp.call(cmd, shell=True)

        fHiteOut = open('hite.out','r')
        hiteline = fHiteOut.readline().split()
        hite = float(hiteline[4])

        # Get t_lock
        qpl = 100
        taupl = 64
          
        rotper=0.33
        obl=60
        model="CPL"

        cpllong[i] = LockTime(num[i],model,mstar[i],rstar[i],mpl[i],rpl[i],rotper,obl,qpl,taupl,semi[i])

        model="CTL"
        ctllong = LockTime(num[i],model,mstar[i],rstar[i],mpl[i],rpl[i],rotper,obl,qpl,taupl,semi[i])

        rotper=10
        obl=0
        model="CPL"
        qpl=10
        taupl=700
        
        cplshort = LockTime(num[i],model,mstar[i],rstar[i],mpl[i],rpl[i],rotper,obl,qpl,taupl,semi[i])

        model="CTL"
          
        ctlshort = LockTime(num[i],model,mstar[i],rstar[i],mpl[i],rpl[i],rotper,obl,qpl,taupl,semi[i])

        qpl=34
        taupl=125
        rotper=1
        obl=23.5
          
        ctlearth = LockTime(num[i],model,mstar[i],rstar[i],mpl[i],rpl[i],rotper,obl,qpl,taupl,semi[i])

        model="CPL"
        cplearth = LockTime(num[i],model,mstar[i],rstar[i],mpl[i],rpl[i],rotper,obl,qpl,taupl,semi[i])

        if (npl[i] == 0):

            fOutFileS.write("%13s %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f " % (num[i],rstar[i],(mstar[i]/MSUN),per[i],rpl[i],mpl[i],semi[i]))
            fOutFileS.write("%.2f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f\n" % (hite,cplshort,cplearth,cpllong[i],ctlshort,ctlearth,ctllong))

            fTexFileS.write("%13s & %6.2f & %6.2f & %6.2f & %6.2f & %6.2f & %6.2f " % (num[i],rstar[i],(mstar[i]/MSUN),per[i],rpl[i],mpl[i],semi[i]))
            fTexFileS.write("%.2f & %6.3f & %6.3f & %6.3f & %6.3f\\\\\n" % (hite,ctlshort,cpllong[i],ctlshort,ctllong))
            if (cpllong[i]*1e6 < 1e3):
                plt.plot(jmag[i],1000,'ro',markersize=(10*hite),markeredgecolor='red',markeredgewidth=0.0)
            else:
                plt.plot(jmag[i],cpllong[i]*1e6,'ro',markersize=(10*hite),markeredgecolor='red',markeredgewidth=0.0)

            if (ctllong*1e6 < 1e3):
                plt.plot(jmag[i],1000,'ko',markersize=(10*hite))
            else:
                plt.plot(jmag[i],ctllong*1e6,'ko',markersize=(10*hite))
        else:
            fOutFileM.write("%13s %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f " % (num[i],rstar[i],(mstar[i]/MSUN),per[i],rpl[i],mpl[i],semi[i]))
            fOutFileM.write("%.2f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f\n" % (hite,cplshort,cplearth,cpllong[i],ctlshort,ctlearth,ctllong))

            fTexFileM.write("%13s & %6.2f & %6.2f & %6.2f & %6.2f & %6.2f & %6.2f " % (num[i],rstar[i],(mstar[i]/MSUN),per[i],rpl[i],mpl[i],semi[i]))
            fTexFileM.write("%.2f & %6.3f & %6.3f & %6.3f & %6.3f\\\\\n" % (hite,cplshort,cpllong[i],ctlshort,ctllong))
            plt.plot(jmag[i],cpllong[i]*1e6,'rx',markersize=(10*hite))
            plt.plot(jmag[i],ctllong*1e6,'kx',markersize=(10*hite))

plt.plot(6.7,6e9,'ko',markersize=10)
plt.plot(6.7,4e9,'ko',markersize=5)
plt.plot(6.7,2.75e9,'ko',markersize=1)
plt.plot(6.9,6e9,'kx',markersize=10)
plt.plot(6.9,4e9,'kx',markersize=5)
plt.plot(6.9,2.75e9,'kx',markersize=1)
plt.text(6.5,1e10,'HITE value')
plt.text(7.05,5.5e9,'1.0')
plt.text(7.05,3.7e9,'0.5')
plt.text(7.05,2.5e9,'0.1')

MakeBox(6.4,7.45,2e9,1.5e10,'k')

plt.plot(7.9,6e9,'ro',markersize=7,markeredgecolor='red',markeredgewidth=0.0)
plt.plot(8.1,6e9,'rx',markersize=7)
plt.plot(7.9,4e9,'ko',markersize=7)
plt.plot(8.1,4e9,'kx',markersize=7)
plt.text(7.9,1e10,'Model')
plt.text(8.2,3.6e9,'CTL')
plt.text(8.2,5.45e9,'CPL',color='r')

MakeBox(7.75,8.6,3e9,1.5e10,'k')

plt.plot(9.15,6e9,'ko',markersize=7)
plt.plot(9.35,6e9,'ro',markersize=7,markeredgecolor='red',markeredgewidth=0.0)
plt.plot(9.15,4e9,'kx',markersize=7)
plt.plot(9.35,4e9,'rx',markersize=7)
plt.text(9,1e10,'Companions')
plt.text(9.45,5.5e9,'Single')
plt.text(9.45,3.6e9,'Multi')

MakeBox(8.9,10.1,3e9,1.5e10,'k')

#plt.show()
#plt.savefig('tesslock.pdf')
plt.savefig('tesslock.eps')

# Clean up eqtide detritus
subp.call("rm *.log *.forward", shell=True)
        
