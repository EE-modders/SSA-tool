
cdef extern from "libblast.c":
    int decompress_bytes(unsigned long l, char* inbuff, char* outf)


cpdef int decompress(unsigned long l, char* inbuff, char* outf):
    return decompress_bytes(l, inbuff, outf)
