# HZPLOT.PY
#
# Plot tidal locking limits relative to the HZ. The files tlockCTL.out and
# tlockCPL.out contain the info for the two models and a 10 and 0.1 Earth-mass
# planet, respectively. These are generated in the TLock sudirectory. To run:
#
# > python hzplot.py
#
import numpy as np
import subprocess as subp
import string
import matplotlib.pyplot as plt

MSUN = 1.98892e33
AUCM = 1.49598e13
RSUN = 6.955e10
LSUN = 3.827e33
PI = 3.1415926535
SIGMA =5.67e-5
YEARSEC = 3600*24*365.25

msmin=0.05  # Minimum stellar mass
msmax=1.3   # Maximum stellar mass
dm=0.001    # Increment in stellar mass

amin=0.05   # Minimum semi-major axis
amax=1.8    # Maximum semi-major axis
da=0.001    # Increment in semi-major axis

# Calculate HZ limits, from Kopparapu et al. (2013)
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
        # For large stellar masses, this can be imaginary, but it doesn't
        # affect the plot or results.
        lim[j] = np.sqrt(lum/seff[j])

def RadLumBoyajian12(r):
    l = -3.5822 + 6.8639*r - 7.185*r**2 + 4.5169*r**3
    return 10**l

def MassLumScalo07(m):
    x=np.log10(m)
    l=4.101*x**3 + 8.162*x**2 + 7.108*x + 0.065
    return 10**l

def MassRadBaraffe15(m):
    return 0.003269 + 1.304*m - 1.312*m**2 + 1.055*m**3

def MassLumBaraffe15(m):
    x=np.log10(m)
    l = -0.0494 + 6.65*x + 8.73*x**2 + 5.208*x**3
    return 10**l

abin=int((amax-amin)/da)       # Number of semi-major axis nodes
mbin=int((msmax-msmin)/dm)     # Number of stellar mass nodes

acol=[0 for i in range(abin)]  # Semi-major axis node values
mcol=[0 for i in range(mbin)]  # Stellar mass node values

l=[0 for i in range(mbin)]     # Stellar luminosity
rs=[0 for i in range(mbin)]    # Stellar radius
teff=[0 for i in range(mbin)]  # Stellar effective temperature
tr=[0 for i in range(mbin)]    # Tidal lock radius from Kasting et al. 1993
rcpl=[0 for i in range(mbin)]  # Tidal lock radius for CPL, 10 Gyr
rctl=[0 for i in range(mbin)]  # Tidal lock radius for CTL, 1 Gyr
rv=[0 for i in range(mbin)]    # Recent Venus
mg=[0 for i in range(mbin)]    # Moist Greenhouse
maxg=[0 for i in range(mbin)]  # Maximum Greenhouse
em=[0 for i in range(mbin)]    # Early Mars
lim=[0 for j in range(6)]

p0 = 13.5     # Initial rotation period from K93

for im in range(mbin):
    mcol[im] = msmin + im*dm
    rs[im] = MassRadBaraffe15(mcol[im])
    l[im] = MassLumBaraffe15(rs[im])
    teff[im]=((l[im]*LSUN)/(4*PI*SIGMA*(rs[im]*RSUN)**2))**0.25
    HabitableZone(l[im],teff[im],lim)
    rv[im] = lim[0]
    mg[im] = lim[2]
    maxg[im] = lim[3]
    em[im] = lim[4]
    tr[im] = 0.027*(13.5*3600 * 4.5e9*YEARSEC / 100)**(1./6) * (mcol[im]*MSUN)**(1./3)
    tr[im] /= AUCM

# Read in extreme limits
t=[[[10.1 for i in range(abin)] for j in range(mbin)] for k in range(2)]

name='tlockCPL.out'
infile=open(name,'r')
print("Reading "+name)

im=0
for line in infile:
    ia=0
    words=str.split(line," ")
    for val in words:
            #print (repr(j)+" "+repr(im)+" "+repr(ia)+": "+val)
        if (val != "\n"):
            t[0][im][ia] = float(val)
            if (ia >0):
                if (t[0][im][ia] > 10 and t[0][im][ia-1] <= 10):
                    rcpl[im]=amin+ia*da

            ia += 1
    im += 1

name='tlockCTL.out'
infile=open(name,'r')
print("Reading "+name)

im=0
for line in infile:
    ia=0
    words=str.split(line," ")
    for val in words:
        if (val != "\n"):
            t[1][im][ia] = float(val)
            if (ia >0):
                if (t[1][im][ia] > 1 and t[1][im][ia-1] <= 1):
                    rctl[im]=amin+ia*da
            ia += 1
    im += 1

fbk = {'lw':0.0, 'edgecolor':None}

plt.figure(figsize=(6.5,9), dpi=200)

plt.xlabel('Semi-Major Axis (AU)',fontsize=20)
plt.ylabel('Stellar Mass (M$_\odot$)',fontsize=20)
plt.tick_params(axis='both', labelsize=20)

xt=[0.01,0.1,1]
yt=[0.1,1]
plt.xscale('log')
plt.yscale('log')
plt.xticks(xt)
plt.yticks(yt)
plt.fill_betweenx(mcol,rv,em,color='0.85', **fbk)
plt.fill_betweenx(mcol,mg,maxg,color='0.75', **fbk)

plt.xlim(0.01,1.75)
plt.ylim(0.08,1.2)

ContSet0 = plt.contour(acol,mcol,t[0],3,colors='black',linestyles='solid',
                       levels=[1,5,10],linewidths=3)
plt.plot(rcpl,mcol,color='k',linestyle='-',linewidth=3,label='CPL, long, 10 Gyr')
plt.plot(rctl,mcol,color='k',linestyle='dotted',linewidth=3,label='CTL, short, 1 Gyr')
plt.plot(tr,mcol,color='r',linestyle='dashed',linewidth=3,label='Kasting et al. (1993)')

plt.legend(loc='upper left')

plt.tight_layout()
plt.savefig('hzplot.eps')


