#!/bin/python3

import argparse
import os
import re
import shutil

parser = argparse.ArgumentParser(description="Get unique hashes from Responder's log files")
parser.add_argument('-c', '--clean', required=False, default='',\
                    help='Move all files in log path to new folder')
parser.add_argument('-t', '--hashtype',  required=False, default='n2', choices=['c', 'n1', 'n2', 'k'],\
                    help='Specify the type of hashes you want to retrieve (default: n2)')
parser.add_argument('-o', '--output', required=False, default='',\
                    help='Output to a file')
parser.add_argument('-p', '--logpath', required=False, default='/usr/share/responder/logs/',\
                    help='Set the location of the files (default: /usr/share/responder/logs')
parser.add_argument('-q', '--quiet', required=False, default=False, action='store_true',\
                    help='Do not print to screen')
args = parser.parse_args()

#print("Have you cleaned up your responder log folder from the last engagement?")
#input("Press CTRL-C to break or ENTER to continue...")
cwd=os.getcwd()

def main(cflag, tflag, oflag, pflag, lflag, qflag):

    # Set hash type search string
    if tflag == 'n1':
        htype = re.compile('NTLM.*v1')
    elif tflag == 'n2':
        htype = re.compile('NTLM.*v2')
    elif tflag == 'k':
        htype = re.compile('Kerberos')
    elif tflag == 'c':
        htype = re.compile('Clear')

    # Get every line of every log file into a list called data
    os.chdir(pflag)
    logfiles = []
    data = []
    for filename in os.listdir(pflag):
        if htype.search(filename):
            logfiles.append(filename)

    for logfile in logfiles:
        with open(logfile,'r') as file:
            line = file.readlines()
        for l in line:
            data.append(l.strip())

    # If clean value is set clean log folder and exit
    if cflag != '':
        moveto = pflag + '/' + cflag
        os.mkdir(moveto)
        for logfile in logfiles:
            shutil.move(logfile, moveto)
        return

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
    # Print the hashes to the screen
    opath = cwd+"/"+oflag
    if qflag == False and oflag == '':
        for q in rhashes:
            print(q)
        print("\nYou have %s unique user hashes!" % len(rhashes))
    elif qflag == True and oflag == '':
        print("You must use the -o flag to specify an output file.")
        oflag=input("Enter the name of the output file: ")
        opath = cwd+"/"+oflag
        with open(opath, 'w') as ofile:
            for q in rhashes:
                ofile.write("%s\n" % q)
    elif qflag == True and oflag != '':
        with open(opath, 'w') as ofile:
            for q in rhashes:
                ofile.write("%s\n" % q)
    elif qflag == False and oflag != '':
        with open(opath, 'w') as ofile:
            for q in rhashes:
                ofile.write("%s\n" % q)
        for q in rhashes:
            print(q)
        print("\nYou have %s unique user hashes!" % len(rhashes))

if __name__ == '__main__':
    main(args.clean, args.hashtype, args.output, args.logpath, args.listtype, args.quiet)
