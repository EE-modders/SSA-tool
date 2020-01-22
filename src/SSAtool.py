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


version = "0.1"

magic_number_compressed = b'PK01'
magic_number_SSA = b'rass'


SSA = SSA()
SSA.read_from_file(sys.argv[1])

SSA.extract(SSA.get_files_list(), SSA.SSAbody)
