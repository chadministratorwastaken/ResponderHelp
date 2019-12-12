#!/bin/python3

import os

print("Have you cleaned up your responder log folder from the last engagement?")
input("Press CTRL-C to break or ENTER to continue...")

# Get every line of every log file into a list called data
logpath = "/usr/share/responder/logs/"
os.chdir(logpath)
logfiles = []
data = []
for filename in os.listdir(logpath):
    if filename.endswith(".txt"):
        logfiles.append(filename)
for logfile in logfiles:
    with open(logfile,'r') as file:
        line = file.readlines()
    for l in line:
        data.append(l.strip())

# Get every unique username from the data
users = []
for r in data:
    u = r.split(':')[0]
    if u not in users:
        users.append(u)

# Get one unique responder hash for each user
rhashes = []
for u in users:
    for h in data:
        if h.find(u) != -1:
            rhashes.append(h)
            break

for q in rhashes:
    print(q)
