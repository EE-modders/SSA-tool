#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22.01.2020 20:08 CET

@author: zocker_160
"""

import os
import sys
import importlib
import lib

from lib.SSA import SSA

importlib.reload(lib)


version = "0.4.2"

magic_number_compressed = b'PK01'
magic_number_SSA = b'rass'
confirm = True
info_only = False
silent = False

def show_help():
    print(
"""USAGE: SSAtool [options] <SSAfile>
or you can just drag & drop the SSA file onto this executable

possible options:
-h, --help, -v  show this help / version information
--info          only show the list of files inside this archive
-nc             "no confirm" disables all confirmation questions
                (useful for batch conversion)
--silent        no output during extract (faster)
""")
    if confirm: input("press Enter to close........")
    sys.exit()

def show_exit():
    input("\npress Enter to close.......\n")
    sys.exit()


def main(inputfile: str, outputfolder: str, decompress=True, log=False):
    # start extraction process
    SSAd = SSA()

    try:
        SSAd.read_from_file(inputfile)
    except TypeError as err:
        print(err.args[0] + "version of the file: " + err.args[1] + err.args[2])
    except ImportError as err:
        print(err.args[0] + "imported magic number: " + err.args[1])

    if info_only:
        SSAd.print_files_list()
        show_exit()

    ## path to output folder has to end with an os.sep
    if outputfolder != "" and not outputfolder.endswith(os.sep):
        outputfolder += os.sep

    if decompress:
        SSAd.extract(SSAd.get_files_list(), SSAd.SSAbody, outputfolder=outputfolder, silent=log, decompress=True)
    else:
        SSAd.extract(SSAd.get_files_list(), SSAd.SSAbody, outputfolder=outputfolder, silent=log)

    print("done!")


if __name__ == "__main__":
    print("### SSA Extractor for Empire Earth made by zocker_160")
    print("### version %s" % version)
    print("""###
### if you have any issue, pls feel free to report it:
### https://github.com/EE-modders/SSA-tool/issues
###
###----------------------------------------------
    """
    )

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
        if arg == "--info":
            info_only = True
            parameter_list.append(i)
        if arg == "--silent":
            silent = True
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

    res = input("Do you want to decompress the files? (Y/n) ")
    if res == "y" or res == "Y" or not res:
        res = True
    else:
        res = False

    main(inputfile=filename, outputfolder=sys.argv[2], decompress=res)

    if confirm: input("press Enter to close.......")
