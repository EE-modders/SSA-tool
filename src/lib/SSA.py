#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22.01.2020 20:08 CET

@author: zocker_160
"""

import os
import sys
from io import BytesIO

class SSA:
    def __init__(self, version_major=0, version_minor=0, data_offset=0, data_body=b''):
        self.header = {
            "magic": b'rass',
            "version_major": version_major,
            "version_minor": version_minor,
            "data_offset": data_offset
        }
        self.SSAbody = data_body
        self.header_length = 16

    def read_from_file(self, filename: str):
        with open(filename, 'rb') as ssafile:            
            read_int_buff = lambda x: int.from_bytes(ssafile.read(x), byteorder="little", signed=False)

            print("parsing........")

            magic = ssafile.read(4)
            if self.header["magic"] != magic:
                raise TypeError("ERROR: this is not a proper SSA file", magic.decode())

            self.header["version_major"] = read_int_buff(4)
            self.header["version_minor"] = read_int_buff(4)
            self.header["data_offset"] = read_int_buff(4)

            if (self.header["version_major"] != 1 or self.header["version_minor"] != 0):
                raise TypeError("ERROR: this version of SSA is not supported", self.header["version_major"], self.header["version_minor"])

            self.SSAbody = ssafile.read(-1)

    def get_files_list(self):
        body_bin = BytesIO(self.SSAbody)                
        file_bin = BytesIO(body_bin.read(self.header["data_offset"]))
        del body_bin

        read_int_buff = lambda x: int.from_bytes(file_bin.read(x), byteorder="little", signed=False)

        files = list()
        
        while True:
            length = file_bin.read(4)
            #print(length)
            if length == b'':
                break
            length = int.from_bytes(length, byteorder="little", signed=False)
            #print(length)
            filename = file_bin.read(length-1) # the string itself is only length - 1 long
            file_bin.read(1) # delimiter 0x00
            files.append( [ filename.decode('ISO-8859-15'), read_int_buff(4), read_int_buff(4), read_int_buff(4) ] )

        return files

    def print_files_list(self):
        files = self.get_files_list()

        output = "SSA files list: \n"

        for file in files:
            output += "name: %s; start offset: %d; end offset: %d; size: %dKiB" % (file[0], file[1], file[2], file[3]/1024)
            output += "\n"

        print(output)
        return files

    def extract(self, files_list: list, ssa_binary: bytes):
        ssa = BytesIO(ssa_binary)
        export_folder = "extracted"

        if not os.path.exists(export_folder): os.makedirs(export_folder)
        os.chdir(export_folder)

        for asset in files_list:
            path = str(asset[0])
            folder = path.split("\\")[0]
            if not os.path.exists(folder):
                os.makedirs(folder)

            # since FUCKING WINDOWS shit has "\" instead "/" like every other normal OS I need to check for it
            if sys.platform[:3] == "lin":
                #print("found Linux: replacing \\ with /")
                path = path.replace("\\", "/")
            #print(path)
            with open(path, 'wb') as newfile:
                ssa.seek(asset[1] - self.header_length) # we need to subtract header length because the SSAbody doesn't contain the header anymore (after read_from_file())
                newfile.write(ssa.read(asset[3]))