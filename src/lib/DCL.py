#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.01.2020 31:01 CET

@author: zocker_160
"""

import ctypes
import os
import subprocess
import sys
import tempfile
from io import BytesIO


class DCL:
    def __init__(self, empty: bool, raw_data=False, data=b''):
        if not empty and not raw_data:
            self.magic, self.uncompressed_size, self.unknown, self.data = self.read_header(data)
        if raw_data:
            self.data = data
    
    def read_header(self, data: bytes):
        fb = BytesIO(data)

        magic = fb.read(4)
        if magic != b'PK01':
            raise TypeError(magic)
        uncompressed_size = fb.read(4)
        unknown = fb.read(4)
        data = fb.read(-1)

        return magic, uncompressed_size, unknown, data

    def decompress(self, outputfile: str):
        current_loc = os.path.dirname(os.path.abspath(__file__))

        if sys.platform[:3] != "win":
            libblast = ctypes.CDLL(os.path.join(current_loc, "libblast.so"))
        else:
            libblast = ctypes.CDLL(os.path.join(current_loc, "libblast.dll"))

        libblast.decompress_bytes.argtypes = [ ctypes.c_ulong, ctypes.c_char_p, ctypes.c_char_p ]    
        libblast.decompress_bytes.restype = ctypes.c_int

        b_outputfile = outputfile.encode()

        return libblast.decompress_bytes(ctypes.c_ulong(len(self.data)), self.data, b_outputfile)


    ## old slow shit, that sucks on Linux use decompress() instead!
    def decompress_sub(self, outputfile: str):
        tmpfile = ""
        tmpname = "DCLTMP"
        os_delimiter = ""
        # check for OS
        if sys.platform[:3] == "win":
            is_windows = True
            os_delimiter = "\\"
        else:  
            is_windows = False
            os_delimiter = "/"

        tmpfile = tempfile.gettempdir() + os_delimiter + tmpname

        # print(os.getcwd())

        # write temp file
        with open(tmpfile, "wb") as tf:
            tf.write(self.data)
                
        if is_windows:
            command = sys._MEIPASS + "\\blast_args.exe " + "\"" + tmpfile + "\" \"" + outputfile + "\""
            #print(command)
            response = subprocess.run(command, stdout=subprocess.PIPE)
            #print(response)
        else:
            command = sys._MEIPASS + "/blast_args " + "\"" + tmpfile + "\" \"" + outputfile + "\""

            response = subprocess.run(command, stdout=subprocess.PIPE)
            #print(response)

        ## print("writing to file")
        #with open(outputfile, "wb") as output:
        #    output.write(response.stdout)
