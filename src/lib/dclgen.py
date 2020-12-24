from distutils.core import Extension, setup
from Cython.Build import cythonize

ext = Extension(
    name="cdcl",
    sources=["dcl.pyx"]
)

setup(ext_modules=cythonize(ext, language_level=3))
