#!/bin/bash
# https://github.com/anhaidgroup/py_entitymatching
# https://sites.google.com/site/anhaidgroup/projects/magellan/py_entitymatching
# A collection of commands used to get Magellan up & running through Docker

# Compile the docker container
make all

# Shell into the docker container
make magellan

# Within the docker container
cd /magellan/py_entitymatching-master/

# Install the dependencies
pip install -r requirements.txt

# Build
python setup.py build

# Setup the program
python setup.py install

# Return to the root dir to execute code from running_magellan.py
cd /root
