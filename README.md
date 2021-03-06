# TideLock
This repository contains all the scripts, data and plots used to generate the manuscript "Tidal Locking of Habitable Exoplanets" to be published in Celestial Mechanics and Dynamical Astronomy. Most of the plots rely on the EQTIDE software package, available at https://github.com/RoryBarnes/EqTide. The scripts which runs EQTIDE through parameter space are all written in python, and I did my best to adhere to the Software Carpentry guidelines outlined in "Good Enough Practices in Scientific Computing" by Wilson et al. (http://adsabs.harvard.edu/abs/2016arXiv160900037W). Each subdirectory contains a README file that describes which figures or tables can be generated from the scripts in the directory, and the scripts are commented, too.

** NOTES **

The caption to Fig. 11 in the paper is incorrect as it states all curves are for a
1 Earth mass planet. In fact, as shown in the HZPlot directory, I used 0.1 and
10 Earth mass planets to find the extremes. Thanks to Hector Rodriguez for catching
this error. 
