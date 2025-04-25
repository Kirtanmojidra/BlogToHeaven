#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files using the correct Python version
python3.10 manage.py collectstatic --noinput
