#!/usr/bin/env bash

# It seems that the API autodocs have some problems processing changes to files.
# This script gives them no choice.

# Run it from the Docs directory with the venv activated

rm -r _build/
make html