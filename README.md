# PyFatFs

Python C extension providing complete bindings for the FatFs library, enabling comprehensive FAT/exFAT filesystem operations.

![Python](https://img.shields.io/badge/python-3.6%2B-blue?logo=python&logoColor=white)
![Last Commit](https://img.shields.io/github/last-commit/Cordagr/EdgeLab)

[Website](#) • [Report an Issue](#) • [Documentation](https://github.com/Cordagr/EdgeLab/wiki) • [Contribute](#)

## Requirements

Before installing PyFatFs, make sure you have:

- Python 3.6+ installed on your system
- Visual Studio Build Tools (Windows) or GCC (Linux/macOS)
- setuptools for building C extensions

## Installation Methods

### From Source

Clone the repository and build locally:

```bash
git clone https://github.com/Cordagr/EdgeLab.git
cd EdgeLab
python setup.py build_ext --inplace
```

### Development Installation

For development, install in editable mode:

```bash
git clone https://github.com/Cordagr/EdgeLab.git
cd EdgeLab
pip install -e .
```

### Using pip (Future)

```bash
pip install pyfatfs
```

*Note: PyPI package not yet available*

## Quick Start

```python
import pyfatfs

# Mount filesystem 
pyfatfs.mount("/", 0, 1)

# Write to a file
with pyfatfs.open_file("HELLO.TXT", "w") as f:
    f.write("Hello, FatFs!")

# Read from a file
with pyfatfs.open_file("HELLO.TXT", "r") as f:
    content = f.read()
    print(content)  # "Hello, FatFs!"
```

## API Reference

### Core Functions
- `mount(path, drive, opt)` - Mount filesystem
- `open_file(path, mode)` - Open file with context manager support
- `close_file(fp)` - Close an open file
- `read_file(fp, size)` - Read data from file
- `write_file(fp, data)` - Write data to file
- `get_error_string(code)` - Get human-readable error messages

### Extended File Operations
- `lseek(fp, offset)` - Move read/write pointer, expand size
- `truncate_file(fp)` - Truncate file size
- `sync_file(fp)` - Flush cached data
- `tell(fp)` - Get current read/write pointer
- `eof(fp)` - Test for end-of-file
- `file_size(fp)` - Get file size
- `file_error(fp)` - Test for file error

### Directory Operations
- `opendir(path)` - Open a directory
- `closedir(dp)` - Close an open directory
- `readdir(dp)` - Read a directory item
- `mkdir(path)` - Create a sub-directory
- `chdir(path)` - Change current directory
- `getcwd()` - Retrieve the current directory

### File and Directory Management
- `stat(path)` - Check existence of a file or sub-directory
- `unlink(path)` - Remove a file or sub-directory
- `rename(old_name, new_name)` - Rename/Move a file or sub-directory
- `chmod(path, attr, mask)` - Change attribute of a file or sub-directory

### Volume Management
- `getfree(path)` - Get free space on the volume
- `getlabel(path)` - Get volume label
- `setlabel(label)` - Set volume label

### High-Level API

#### File Manager
```python
from pyfatfs.FileAccessWrapper import FatFsFileManager

manager = FatFsFileManager()
manager.mount_filesystem("/", 0, 1)

# File operations
with manager.open_file("test.txt", "w") as f:
    f.write("Hello World!")

info = manager.get_file_info("test.txt")
manager.copy_file("test.txt", "backup.txt")
manager.rename_file("test.txt", "renamed.txt")
manager.delete_file("backup.txt")
```

#### Directory Manager
```python
from pyfatfs.DirectoryAccessWrapper import FatFsDirectoryManager

# Directory operations
FatFsDirectoryManager.create_directory("mydir")
entries = FatFsDirectoryManager.list_directory("/")
exists = FatFsDirectoryManager.file_exists("myfile.txt")
info = FatFsDirectoryManager.get_file_info("myfile.txt")
```

### File Modes
- `"r"` - Read only, `"w"` - Write (truncate), `"a"` - Append
- `"r+"` - Read/write (must exist), `"w+"` - Read/write (truncate)

### File Access Flags (Low-level)
- `FA_READ` - Read access
- `FA_WRITE` - Write access
- `FA_OPEN_EXISTING` - Open existing file only
- `FA_CREATE_NEW` - Create new file only
- `FA_CREATE_ALWAYS` - Create new or truncate existing
- `FA_OPEN_ALWAYS` - Open existing or create new
- `FA_OPEN_APPEND` - Open for append

### File Attributes
- `AM_RDO` - Read only
- `AM_HID` - Hidden
- `AM_SYS` - System
- `AM_DIR` - Directory
- `AM_ARC` - Archive

## Features

 **Complete FatFs API Coverage**
- All file access functions (f_open, f_close, f_read, f_write, f_lseek, f_truncate, f_sync, etc.)
- All directory access functions (f_opendir, f_closedir, f_readdir)
- All file/directory management functions (f_stat, f_unlink, f_rename, f_chmod, f_mkdir, etc.)
- All volume management functions (f_mount, f_mkfs, f_getfree, f_getlabel, f_setlabel)

 **High-Level Python Interface**
- Context manager support for automatic resource cleanup
- Pythonic file and directory operations
- Enhanced error handling with descriptive messages
- File manager for advanced operations

 **Cross-Platform Compatibility**
- Windows, Linux, macOS support
- Virtual disk support for testing
- No external dependencies beyond build tools

## Next Steps

- Check out [test_comprehensive.py](test_comprehensive.py) for complete usage examples
- Explore the high-level API for easier Python integration
- Review [FatFs documentation](http://elm-chan.org/fsw/ff/00index_e.html) for advanced features

## Credits

- FatFs library by ChaN 
- [FatFS Tool](https://elm-chan.org/fsw/ff/)

## Support

For issues and questions:

1. Check the examples directory
2. Review the API documentation
3. Open an issue on the repository
4. Check FatFs documentation for low-level details

## License

This project is licensed under the MIT License.
