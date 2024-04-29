# LhARAlinearOptics
Linear optics code for LhARA -- Tag1

The code in this repository provides linear beam-line optics code and implemetations of the DRACO, LION< and LhARA Stage 1 beamlines.  

## To set up and run:
A guide to setting up and running the package is given in 00-Documentation/00-Setup-n-run/Setup-n-run.pdf.

Execute "startup.bash" from this directory (i.e. run the bash command "source startup.bash").  This will:
  * Set up "LhARAOpticsPATH"; and
  * Add "01-Code" to the PYTHONPATH.  The scripts in "02-Tests" may then be run with the command "python 02-Tests/<filename>.py".

## Directories:
 * Python classes and "library" code stored in "01-Code"
 * Test scripts stored in "02-Tests"
 * Parameters to control the run conditions are stored in "11-Parameters"
 * Example scripts are provided in "03-Scripts"
 * An example user directory is provided in 31-UserDirectory

Rudimentary, but, goal is one test script per class/package file in 01-Code.

## Dependencies:
 * Code and test scripts assume Python 3.  
 * Test scripts assume code directory (01-Code) is in PYTHON path.  A bash script "startup.bash" is provided to update the PYTHON path.

## History
 * January 2024:  Code tidied for "users"/co-developers!

## Updating to new install and set-up -- read this:
 * git clone git@github.com:ImperialCollegeLondon/LhARAlinearOptics.git
 * cd LhARAlineaOptics
 * python3 python3 -m venv venv
 * source ./venv/bin/activate
 * pip install -r ./requirements.txt
 
 * source setup.bash                