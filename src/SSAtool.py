#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22.01.2020 20:08 CET

@author: zocker_160
"""

import sys
import importlib
import lib

from lib.SSA import SSA

importlib.reload(lib)


version = "0.1 alpha"

magic_number_compressed = b'PK01'
magic_number_SSA = b'rass'
confirm = True
short_output = False

print("### SSA Extractor for Empire Earth made by zocker_160")
print("### version %s" % version)
print("###")
print("### if you have any issue, pls feel free to report it:")
print("### https://github.com/EE-modders/SSA-tool/issues")
print("###")
print("###----------------------------------------------\n")

def show_help():
    print("USAGE: SSAtool [options] <SSAfile>")
    # TODO: "--info" (show header information only)
    print()
    print()
    print("possible options:")
    print("-h, --help, -v\tshow this help / version information")
    #print("-nc\t\t\"no confirm\" disables all confirmation questions\n\t\tuseful for batch conversion")
    #print("-so\t\t\"short output\" doesn't add \"_NEW_\" to the output SST file")
    if confirm: input("press Enter to close........")
    sys.exit()

def show_exit():
    input("\npress Enter to close.......\n")
    sys.exit()

if len(sys.argv) <= 1:
    show_help()


parameter_list = list()

for i, arg in enumerate(sys.argv):
    if arg == "-h" or arg == "--help" or arg == "-v":
        confirm = False
        show_help()
    if arg == "-nc":
        confirm = False
        parameter_list.append(i)        
    if arg == "-so":
        short_output = True
        parameter_list.append(i)        

# remove commandline parameters
parameter_list.sort(reverse=True)
for param in parameter_list:
    sys.argv.pop(param)

try:
    filename = sys.argv[1]
except IndexError:
    print("ERROR: no file(s) specified!")
    show_exit()

if filename.split('.')[-1] != "ssa":
    print("ERROR: invalid input file!")
    show_exit()


# start extraction process
SSA = SSA()

try:
    SSA.read_from_file(sys.argv[1])
except TypeError as err:
    print(err.args[0] + "version of the file: " + err.args[1] + err.args[2])
except ImportError as err:
    print(err.args[0] + "imported magic number: " + err.args[1])

SSA.extract(SSA.get_files_list(), SSA.SSAbody)

print("done!")

if confirm: input("press Enter to close.......")
