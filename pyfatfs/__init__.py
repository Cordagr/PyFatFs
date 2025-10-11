"""
PyFatFs - Python bindings for the FatFs library

A high-level, Pythonic interface for file and directory management
using the FatFs library for embedded systems and microcontrollers.
"""

from . import core
from .file import FatFsFile, open_file, read_file_content, write_file_content, append_file_content

__version__ = "0.1.0"
__author__ = "PyFatFs Contributors"

# Convenience imports
mount = core.mount
get_error_string = core.get_error_string

# File access constants
FA_READ = core.FA_READ
FA_WRITE = core.FA_WRITE
FA_OPEN_EXISTING = core.FA_OPEN_EXISTING
FA_CREATE_NEW = core.FA_CREATE_NEW
FA_CREATE_ALWAYS = core.FA_CREATE_ALWAYS
FA_OPEN_ALWAYS = core.FA_OPEN_ALWAYS
FA_OPEN_APPEND = core.FA_OPEN_APPEND

# Result codes
FR_OK = core.FR_OK
FR_DISK_ERR = core.FR_DISK_ERR
FR_NOT_READY = core.FR_NOT_READY
FR_NO_FILE = core.FR_NO_FILE
FR_NO_PATH = core.FR_NO_PATH
FR_INVALID_NAME = core.FR_INVALID_NAME
FR_DENIED = core.FR_DENIED
FR_EXIST = core.FR_EXIST

__all__ = [
    'core',
    'FatFsFile', 
    'open_file', 
    'read_file_content', 
    'write_file_content', 
    'append_file_content',
    'mount',
    'get_error_string',
    'FA_READ', 'FA_WRITE', 'FA_OPEN_EXISTING', 'FA_CREATE_NEW', 
    'FA_CREATE_ALWAYS', 'FA_OPEN_ALWAYS', 'FA_OPEN_APPEND',
    'FR_OK', 'FR_DISK_ERR', 'FR_NOT_READY', 'FR_NO_FILE', 
    'FR_NO_PATH', 'FR_INVALID_NAME', 'FR_DENIED', 'FR_EXIST'
]