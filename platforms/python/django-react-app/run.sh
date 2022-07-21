#!/usr/bin/env bash

# exit on first error
set -e

# activate virtual environment
source .venv/bin/activate

# Install (or update) requirements
pip install -r requirements.txt

./manage.py runserver