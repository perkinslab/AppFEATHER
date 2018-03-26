# Description

This repository contains FEATHER (*F*orce *E*xtension *A*nalysis using a *T*estable *H*ypothesis for *E*vent *R*ecognition), a freely available technique for finding rupture events in force spectroscopy data.

# Citing FEATHER

If you use FEATHER, please use the following citation:

xxx

# Installing

## Getting the Repository

To install, in git bash (for windows, https://git-scm.com/downloads) or Terminal (Mac/OS), type in the following:

git clone --recurse-submodules https://github.com/prheenan/AppFEATHER.git

This will install FEATHER to the current directory. 

## Dependencies

Although FEATHER has interfaces for Matlab (tested with version 2017a), Igor (tested with 6.37 and 7.04), and Python (2.7), Python 2.7 is needed for FEATHER. The easiest way to install Python 2.7 and the dependencies is the free Anaconda:

https://www.anaconda.com/download

Again, install python2.7 (*not* python3.4). For Matlab and Igor usage, FEATHER assumes there will be a python binary (or .exe for Windows) at:

- "C:/ProgramData/Anaconda2/" (for Windows)
- "//anaconda/bin/python2" (for MAC/Linux)

As of 2018-3-26, the above paths are the default option for when Anaconda installs. If you install to a different location and use Matlab or Igor, you will need to update the relevant path in the ".m" or ".ipf" (see below).

You will need the following libraries

- numpy
- scipy

# Running the example

Each language (Matlab, Python, and Igor Pro) has an example file which shows FEATHER working on a polyprotein force-extension curve. The files are located in AppYYY, where YYY is the language name. In particular:

- Matlab: Run 'feather_example.m' in the AppMatlab folder
- Igor Pro: 
	- Open 'Example/MainFEATHER.ipf' in the AppIgor folder
	- Run 'ModMainFeather#Main_Windows()' in the command window after compiling
- Python:
	- Run 'main_unit_feather.py' from the AppPython/UnitTest folder
	- e.g. For windows type 'C:/ProgramData/Anaconda2/python main_unit_feather.py' without quotes for Windows in git bash




