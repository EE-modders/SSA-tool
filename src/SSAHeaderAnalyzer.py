#! /usr/bin/env python3 

import sys
import struct

VERSION = "0.4"

def show_info():
    print("### SSA Header analyzer for Empire Earth made by zocker_160")
    print("### version %s" % VERSION)
    print("###")
    print("### if you have any issue, pls feel free to report it:")
    print("### https://github.com/EE-modders/SSA-tool/issues")
    print("###")
    print("###----------------------------------------------\n")

def show_exit():
    input("\npress Enter to close.......\n")
    sys.exit()



if __name__ == "__main__":
    show_info()

    try:
        with open(sys.argv[1], "rb") as ssafile:
            readInt = lambda: struct.unpack("<I", ssafile.read(4))[0]

            print("magic:", ssafile.read(4))

            version_major = readInt()
            version_minor = readInt()
            print(f"SSA version: v{version_major}.{version_minor}")

            print("Data start offset:", readInt())

            nameLen = readInt()
            print("First entry length:", nameLen)
            print("First entry name:", ssafile.read(nameLen-1).decode())

            print("Used delimiter:", ssafile.read(1))

            print("First entry start offset:", readInt())
            print("First entry end offset:", readInt())
            print("First entry size in bytes:", readInt())
    except IndexError:
        print("ERROR: please specify an SSA file!")
    except FileNotFoundError:
        print("ERROR: could not find specified file!")
    finally:
        show_exit()
