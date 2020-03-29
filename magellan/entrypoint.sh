#!/bin/bash

cd /magellan/py_entitymatching/

pip install -r requirements.txt

python setup.py install

exec "$@"
