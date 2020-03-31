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


version = "0.4"

magic_number_compressed = b'PK01'
magic_number_SSA = b'rass'
confirm = True
short_output = False
info_only = False

print("### SSA Extractor for Empire Earth made by zocker_160")
print("### version %s" % version)
print("###")
print("### if you have any issue, pls feel free to report it:")
print("### https://github.com/EE-modders/SSA-tool/issues")
print("###")
print("###----------------------------------------------\n")

def show_help():
    print("USAGE: SSAtool [options] <SSAfile>")
    print("or you can just drag & drop the SSA file onto this executable")
    print()
    print("possible options:")
    print("-h, --help, -v\tshow this help / version information")
    print("--info\t\tonly show the list of files inside this archive")
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
    if arg == "--info":
        info_only = True
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

if info_only:
    SSA.print_files_list()
    show_exit()

res = input("Do you want to decompress the files? (y/n) ")

if res == "y":
    SSA.extract(SSA.get_files_list(), SSA.SSAbody, True)
elif res == "n":
    SSA.extract(SSA.get_files_list(), SSA.SSAbody)
else:
    print("ERROR: invalid input!")
    show_exit()

print("done!")

if confirm: input("press Enter to close.......")
