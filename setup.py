from distutils.core import setup
from Cython.Build import cythonize

setup(name="tvd", ext_modules=cythonize("tvd/*.py"))
