#!/bin/bash

#.. Parse arguments:
debug="false"
while getopts ":dp:" opt; do
    case $opt in
	d) debug="true" ;;
	p) path=$OPTARG ;;
    esac
done
if [ $OPTIND -eq 1 ];
then
    echo "Usage: startup -p <path to LhARA optics code> [-d]"
    return 1
fi

if [ $debug == "true" ]; then
    echo "Debug              :" $debug
    echo "Path to LhARAOptics:" $path
fi


if [ -n "$path" ]
then
    StartUpScript="$path/startup.bash"
    scriptPATH=$(realpath ${StartUpScript})
    if [ $debug == "true" ]; then
	echo "source $scriptPATH"
	source "$scriptPATH"
    else
	source "$scriptPATH"
    fi
fi

add="/01-Code"
dir="$HOMEPATH$add"
if [ -z ${PYTHONPATH+x} ]; then
    PYTHONPATH=":$dir"
else
    PYTHONPATH="$dir:${PYTHONPATH}"
fi
if [ $debug == "true" ]; then
    echo "Python path set:"
    echo "    " $PYTHONPATH
fi
export PYTHONPATH
