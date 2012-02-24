# Ondina Usage Log Suite

## `cpu_monitor.py`

This program collects per-user CPU time every five seconds and writes it
to a log file.

### Usage

        python3.2 cpu_monitor.py mylog.bin


### File format

The output file specified by the first argument is a binary file containing
three values per log entry:

 - Time of day in seconds since epoch
 - CPU time used in 10,000 250th of a jiffy
 - UID of the user

Each log entry is 12 bytes in size, that is 4 bytes for each of the fields
which are big-endina integers (from \x00\x00\x00\x00 to \xff\xff\xff\xff)
