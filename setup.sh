#!/bin/sh

sudo apt-get install ncbi-blast+
source .envrc
source venv/bin/activate
FLASK_APP=app.py
flask run --host=0.0.0.0