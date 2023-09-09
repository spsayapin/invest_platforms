import sys

import os

INTERP = os.path.expanduser("/var/www/u2230134/data/flaskenv/bin/python")
if sys.executable != INTERP:
   os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from app import application