#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22.01.2020 20:08 CET

@author: zocker_160
"""

import os
import sys
import argparse

if __name__ == "__main__":
    import importlib
    import lib
    importlib.reload(lib)
    
    from lib.SSA import SSA
else:
    from .lib.SSA import SSA


VERSION = "0.4.3"

magic_number_compressed = b'PK01'
magic_number_SSA = b'rass'


def show_info():
    print("### SSA Extractor for Empire Earth made by zocker_160")
    print("### version %s" % VERSION)
    print("###")
    print("### if you have any issue, pls feel free to report it:")
    print("### https://github.com/EE-modders/SSA-tool/issues")
    print("###")
    print("###----------------------------------------------\n")


def show_exit():
    input("\npress Enter to close.......\n")
    sys.exit()


def main(inputfile: str, outputfolder: str, decompress=True, log=False, encoding=None):
    # start extraction process
    SSAd = SSA()

    try:
        SSAd.read_from_file(inputfile)
    except TypeError as err:
        print(err.args[0] + "version of the file: " + err.args[1] + err.args[2])
    except ImportError as err:
        print(err.args[0] + "imported magic number: " + err.args[1])

    ## path to output folder has to end with an os.sep
    if outputfolder != "" and not outputfolder.endswith(os.sep):
        outputfolder += os.sep

    if encoding:
        SSAd.extract(SSAd.get_files_list(char_encoding=encoding), SSAd.SSAbody, outputfolder=outputfolder, silent=log, decompress=decompress)
    else:
        SSAd.extract(SSAd.get_files_list(), SSAd.SSAbody, outputfolder=outputfolder, silent=log, decompress=decompress)

    print("done!")

def showFileList(inputfile: str):
    SSAi = SSA()
    SSAi.read_from_file(inputfile)
    SSAi.print_files_list()

def getFileList(inputfile: str, encoding=None) -> list:
    SSAi = SSA()
    SSAi.read_from_file(inputfile)

    if encoding:
        return SSAi.get_files_list(char_encoding=encoding)
    else:
        return SSAi.get_files_list()


def cli_params():
    parser = argparse.ArgumentParser(description="SSA Extractor for Empire Earth made by zocker_160", epilog="You can also just drag & drop the SSA file onto this executable!")

    parser.add_argument("SSAfile", help="SSA archive file")

    #parser.add_argument("-nc", dest="confirm", action="store_true", help="\"no confirm\" disables all confirmation questions (useful for batch conversion)")
    parser.add_argument("-i", "--info", dest="info_only", action="store_true", help="only show the list of files inside this archive")
    #parser.add_argument("-s", "--silent", dest="silent", action="store_true", help="no output during extract (faster)")
    parser.add_argument("-v", "--version", action="version", version=VERSION)

    return parser.parse_args()

if __name__ == "__main__":
    show_info()

    CLI = cli_params()

    #print(CLI)

    filename: str = CLI.SSAfile
    info_only: bool = CLI.info_only

    if not filename.endswith(".ssa"):
        print("ERROR: invalid input file! Only SSA is supported!")
        show_exit()

    if info_only:
        showFileList(filename)
        show_exit()

    res = input("Do you want to decompress the files? (Y/n) ")
    if res == "y" or res == "Y" or not res:
        res = True
    else:
        res = False

    main(inputfile=filename, outputfolder="", decompress=res)

    show_exit()
