from distutils.core import setup
from Cython.Build import cythonize

setup(name="topoprm", ext_modules=cythonize("topoprm/*.py"))
