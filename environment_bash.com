#!/bin/bash 

# . Bash environment variables and paths to be added to a user's ".bash_profile" file.
# . Some modifications may be necessary to work properly (e.g. GTKDYNAMO_ROOT and PYTHONPATH).

GTKDYNAMO_ROOT=/home/fernando/Documents/gtkdynamo2 ; export GTKDYNAMO_ROOT