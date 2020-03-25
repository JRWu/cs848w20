#!/bin/bash

# Compile the docker container
make all

# Shell into the docker container
make dedupe

# Within the docker container
cd /dedupe/dedupe-examples-master

# Install the dependencies for the examples
pip install -r requirements.txt

# Try the csv_example
python csv_example.py

# labeled 
# 20 records

# Evaluate the results, using csv_example_training.json
python csv_evaluation.py





