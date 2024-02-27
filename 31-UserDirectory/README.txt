README.txt
==========

To set up code, execute:

source startup.bash -p /vols/ccap/packages/LhARA/LhARAlinearOptics

Then, the environment variables specific for LhARAlinearOptics will be set up.

You'll need to enter your virtual environment as described in:

$LhARAlinearOptics/00-Documentation/00-Setup-n-run/LhARA-Beamline-01.pdf

Now you should be able to copy the parameter files you want into your local parameters directory, e.g.:

cp $LhARAlinearOptics/11-Parameters/LIONBeamLine-Params-LsrDrvn.* 11-Parameters/.

And execute the scripts, e.g.:

cp $LhARAlinearOptics/03-Scripts/RunLIONsimulation.py
