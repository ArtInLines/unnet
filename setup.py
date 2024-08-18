from setuptools import setup
from Cython.Build import cythonize

setup(
    name='unnet',
    ext_modules=cythonize("unnet.py"),
    version="0.0.1",
    description="Network analysis for UN resolutions",
    author="ArtInLines",
    url="https://github.com/artInLines/unnet",
    license="MIT"
)