#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.01.2020 31:01 CET

@author: zocker_160
"""

import sys
import os
# import ctypes
import tempfile
import subprocess
from io import BytesIO

class DCL:
    def __init__(self, header: bool, data=b''):
        if header:
            self.magic, self.size, self.unknown, self.data = self.read_header(data)
        else:
            self.magic = b'PK01'
            self.unknown = b'\x00\x00\x00\x00'
            self.data = data
    
    def read_header(self, data: bytes):
        fb = BytesIO(data)

        magic = fb.read(4)
        if magic != b'PK01':            
            raise TypeError(magic)
        size = fb.read(4)
        unknown = fb.read(4)
        data = fb.read(-1)

        return magic, size, unknown, data

    def set_header(self, size: int, data: bytes):
        self.size = size.to_bytes(4, byteorder='little', signed=False)
        self.data = data

    def get_header_bytes(self):
        output = b''
        output += self.magic
        output += self.size
        output += self.unknown
        return output

    # def decompress(self, outputfile: str):
    #     tmpfile = ""
    #     tmpname = "DCLTMP"
    #     os_delimiter = ""
    #     # check for OS
    #     if sys.platform[:3] != "win":
    #         is_windows = False
    #     else:  
    #         is_windows = True
    # 
    #     # print(os.getcwd())
    #     if is_windows:
    #         os_delimiter = "\\"
    #         decompressor = ctypes.cdll.LoadLibrary("..\\lib\\blast_old\\libblast.dll")
    #     else:
    #         os_delimiter = "/"
    #         decompressor = ctypes.cdll.LoadLibrary("../lib/blast_old/libblast.so")
    #         
    #     tmpfile = tempfile.gettempdir() + os_delimiter + tmpname
    # 
    #     # string_in = tmpfile.encode('ISO-8859-15')
    #     # string_out = outputfile.encode('ISO-8859-15')
    # 
    #     string_in = tmpfile.encode('utf-8')
    #     string_out = outputfile.encode('utf-8')
    # 
    # 
    #     # write tempfile
    #     with open(tmpfile, "wb") as tmpfile:
    #         tmpfile.write(self.data)
    # 
    #     result = decompressor.main(ctypes.c_char_p(string_in), ctypes.c_char_p(string_out))
    # 
    #     if result != 0:
    #         print("ERROR: %s" % result)
    #         print(outputfile)
    #         #print(outputfile.split(os_delimiter)[-2] + os_delimiter + outputfile.split(os_delimiter)[-1])

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
    
    def decompress_sub2(self, outputfile: str):
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
        
        print("decompress.....")
        # write temp file
        with open(tmpfile, "wb") as tf:
            tf.write(self.data)

        if is_windows:
            command = sys._MEIPASS + "\\exploder.exe " + "\"" + tmpfile + "\""
            print(command)            
        else:            
            #command = sys._MEIPASS + "/exploder " + "\"" + tmpfile + "\""        
            print(os.getcwd())
            # this is only for debugging and if you don't use pyinstaller!            
            command = "./lib/exploder " + "\"" + tmpfile + "\""

        response = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
        #print(response)

        # print("writing to file")
        with open(outputfile, "wb") as output:
            output.write(response.stdout)

    def compress_sub(self, outputfile: str):
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

        # write temp file
        with open(tmpfile, "wb") as tf:
            tf.write(self.data)

        if is_windows:
            command = sys._MEIPASS + "\\imploder.exe " + "\"" + tmpfile + "\""
            #print(command)            
        else:
            # print("decompress.....")
            #command = sys._MEIPASS + "/exploder " + "\"" + tmpfile + "\""        
            print(os.getcwd())
            # this is only for debugging and if you don't use pyinstaller!            
            command = "./lib/imploder " + "\"" + tmpfile + "\""

        response = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
        #print(response)

        compressed_file = self.get_header_bytes() + response.stdout

        # print("writing to file")
        with open(outputfile, "wb") as output:
            output.write(compressed_file)

        return compressed_file