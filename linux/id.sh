#!/bin/bash

#This script integrates the display of SGD to a putty session.
#Please run this script first on SGD only to interate the display to puTTY.

mkdir disp_env

cd disp_env
echo $DISPLAY
echo $DISPLAY > display_var
