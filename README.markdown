Usage Log
---------

This program logs CPU and memory usage on a per user basis,
at randomised intervals. 

It's written in Python 3000. To run it, type

python3.2 usage_log.py

The log will be written to the current working directory.
It contains one json-encoded object per line. The objects
are dictionaries mapping the current date and time to the
users mapped to their cpu and memory usage in percent as
reported by ps.
