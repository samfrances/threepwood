#! /bin/bash

# This is an example script to be run on a regular schedule by cron,
# which sets up the correct virtualenv for the threepwood bot

cd /path/to/threepwood/directory # path to directory of threepwood repo
source venv/bin/activate		 # assumes virtualenv called venv

# virtualenv is now active, which means your PATH has been modified.
# Don't try to run python from /usr/bin/python, just run "python" and
# let the PATH figure out which version to run (based on what your
# virtualenv has configured).

python bot.py
