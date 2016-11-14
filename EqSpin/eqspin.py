#
# EQSPIN.PY
#
# Calculate equilibrium or psuedo-synchronous spin period for different
# assumptions. To run:
#
# > python eqspin.py


import numpy as np
import matplotlib.pyplot as plt

ecc=[j/1000. for j in range(500)]
ctl=[0 for j in range(500)]
cpl=[0 for j in range(500)]
g66=[0 for j in range(500)]

for j in range(500):
    ctl[j] = 1+6*ecc[j]**2
    g66[j] = 1+9.5*ecc[j]**2
    if ecc[j] < np.sqrt(1./19):
        cpl[j] = 1
    else:
        cpl[j] = 1.5

plt.figure(figsize=(6.5,8), dpi=200)

plt.xlim(0,0.4)
plt.ylim(0.95,2.5)
xt=[0,0.1,0.2,0.3,0.4]
plt.xticks(xt)
plt.tick_params(axis='both', labelsize=20)
plt.ylabel('$\Omega_{eq}$ /n',fontsize=20)
plt.xlabel('Eccentricity',fontsize=20)
plt.plot(ecc,cpl,linestyle='-',color='k',linewidth=2,label='CPL')
plt.plot(ecc,ctl,linestyle='dashed',color='k',linewidth=2,label='CTL')
plt.plot(ecc,g66,linestyle='dotted',color='k',linewidth=2,label='Goldreich66')
plt.legend(loc='upper left')

plt.tight_layout()
plt.savefig('eqspin.eps')
