#!/usr/bin/env bash

pyvenv venv

source ./venv/bin/activate

# This script first tries to build wheels for required packages.  Skips if wheel already exists.
# Install packages from wheels.

# Install wheel package
pip install wheel

# Build & install support packages
pip wheel -r req-common.txt
pip install -U -r req-common.txt

# Freeze package version numbers
pip freeze > req-stable.txt


#################################################
# IPython stuff

# This path will differ between home and work computers.
FOLDER="/home/pierre/Projects/ipython"

if [ -d "$FOLDER" ]
then
    # Folder does exist, perform update.
    cd $FOLDER
    git pull

    git submodule update
else
    # Folder does not exist
    git clone --recursive git://github.com/ipython/ipython.git $FOLDER
    cd $FOLDER

    git submodule update
fi


# Clone specific revision??
# http://stackoverflow.com/questions/3555107/git-clone-particular-version-of-remote-repository
# http://git-scm.com/docs/git-clone
# http://git-scm.com/docs/git-log

# HASH_NUMBER="HEAD"
HASH_NUMBER="b76f8a02a8c7d3fa93d2bdfc111338448886dd0a"  # 2014-11-25

# git rev-list --date-order --max-count=1 HEAD
git reset --hard $HASH_NUMBER

# Install
pip install -U .

# Put ipython repo back to HEAD.
git reset --hard HEAD
