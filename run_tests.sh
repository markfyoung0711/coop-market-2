#!/bin/bash
mydir=$(readlink -f $(dirname $0))
cd $mydir
. ./setup.sh
export PYTHONPATH=$PWD:$PYTHONPATH
pytest -v --capture=no
