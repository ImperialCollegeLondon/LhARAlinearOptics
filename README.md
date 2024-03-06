# LhARALinearOptics
Fork of a linear optics code for the LhARA beamline.

The code in this repository provides linear beam-line optics code and implemetations of the LhARA Stage 1 beamlines.

## To set up and run:

Execute "startup.bash" from this directory (i.e. run the bash command "source startup.bash").  This will:
  * Set up "LhARAOpticsPATH"; and
  * Add "01-Code" to the PYTHONPATH.  The scripts in "02-Tests" may then be run with the command "python 02-Tests/<filename>.py".

## Directories:
 * Python classes and "library" code stored in "01-Code"
 * Test scripts stored in "02-Tests"
 * Parameters to control the run conditions are stored in "11-Parameters"
 * Example scripts are provided in "03-Scripts"

## Dependencies:
 * Code and test scripts assume Python 3.  
 * Test scripts assume code directory (01-Code) is in PYTHON path.  A bash script "startup.bash" is provided to update the PYTHON path.

