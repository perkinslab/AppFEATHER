#!/bin/bash
# courtesy of: http://redsymbol.net/articles/unofficial-bash-strict-mode/
# (helps with debugging)
# set -e: immediately exit if we find a non zero
# set -u: undefined references cause errors
# set -o: single error causes full pipeline failure.
set -euo pipefail
IFS=$'\n\t'
# datestring, used in many different places...
dateStr=`date +%Y-%m-%d:%H:%M:%S`

# Description:

# Arguments:
#### Arg 1: Description

# test matlab
cd ../AppMatlab/
matlab_binary="/Applications/MATLAB_R2017a.app/bin/matlab"
"${matlab_binary}" -nodesktop  -nosplash -r "run('feather_example.m'); exit;"
cd - > /dev/null
# test python
cd ../AppPython/
python2 main_example.py || ( echo "Runing python2 failed" ; exit );
python3 main_example.py || ( echo "Runing python3 failed" ; exit );
cd - > /dev/null



# Returns:



