from setuptools import setup
from Cython.Build import cythonize

setup(
    name='unnet',
    ext_modules=cythonize("unnet.py"),
)