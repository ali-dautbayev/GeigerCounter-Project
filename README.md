# GeigerCounter-Project

Repository for my Geiger counter project containing:

/main:
**GM-CounterProj.pdf**  - Project report containing construction, calibration, and data results

/data:
**data.csv** - Raw data from calibration at background radiation
**counts.txt** - Counts per minute (CPM) for many one-minute intervals

/scripts:
**readinput.py** - Reads input from Arduino and writes to CSV file
**makegraph.py** - Reads the realtime CSV file and makes a live graph
