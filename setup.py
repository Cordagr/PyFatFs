from setuptools import setup, Extension
import os

# Define the C extension
fatfs_extension = Extension(
    'fatfs',
    sources=[
        'source/ff.c',
        'source/diskio_working.c',
        'source/ffsystem.c',
        'source/ffunicode.c',
        'source/fatfs_python.c',
    ],
    include_dirs=['source'],
    define_macros=[],
)

setup(
    name='pyfatfs',
    version='0.1.0',
    description='Python bindings for FatFs library',
    packages=['pyfatfs'],
    ext_modules=[fatfs_extension],
    python_requires='>=3.6',
)