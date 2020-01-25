import sys
import ctypes
import subprocess

def call_subprocess():
    inputfile = open(sys.argv[1])

    response = subprocess.run("./blast", stdin=inputfile, stdout=subprocess.PIPE)

    print("writing ot file")

    with open("test_decompressed.pk", "wb") as output:
        output.write(response.stdout)

def call_clib():
    decomp = ctypes.cdll.LoadLibrary("./libblast.so")

    outputfilename = sys.argv[1].split('.')[0] + "_decomp" + "." + sys.argv[1].split('.')[-1]

    fileobject = open(sys.argv[1], "rb")
    outfileobject = open(outputfilename, "wb")

    fid = fileobject.fileno()
    oid = outfileobject.fileno()

    #print(fid)
    #print()

    outputbytes = decomp.main(fid, oid)

    # print(outputbytes)

    fileobject.close()
    outfileobject.close()

    # with open(outputfilename, "wb") as output:
    #     output.write(outputbytes)

def call_clib_str():
    decomp = ctypes.cdll.LoadLibrary("./libblast.so")

    inputfilename = sys.argv[1]
    outputfilename = sys.argv[1].split('.')[0] + "_decomp" + "." + sys.argv[1].split('.')[-1]

    c_string_in = inputfilename.encode("utf-8")
    c_string_out = outputfilename.encode("utf-8")

    outputbytes = decomp.main(ctypes.c_char_p(c_string_in),  ctypes.c_char_p(c_string_out))

    print(outputbytes)

call_clib_str()
