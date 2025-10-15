"""
Core FatFs bindings - Low-level interface to the compiled FatFs library
"""
import fatfs  # Import our compiled C extension

# FatFs result codes
FR_OK = 0                 # Succeeded
FR_DISK_ERR = 1           # A hard error occurred in the low level disk I/O layer
FR_INT_ERR = 2            # Assertion failed
FR_NOT_READY = 3          # The physical drive cannot work
FR_NO_FILE = 4            # Could not find the file
FR_NO_PATH = 5            # Could not find the path
FR_INVALID_NAME = 6       # The path name format is invalid
FR_DENIED = 7             # Access denied due to prohibited access or directory full
FR_EXIST = 8              # Access denied due to prohibited access
FR_INVALID_OBJECT = 9     # The file/directory object is invalid
FR_WRITE_PROTECTED = 10   # The physical drive is write protected
FR_INVALID_DRIVE = 11     # The logical drive number is invalid
FR_NOT_ENABLED = 12       # The volume has no work area
FR_NO_FILESYSTEM = 13     # There is no valid FAT volume
FR_MKFS_ABORTED = 14      # The f_mkfs() aborted due to any problem
FR_TIMEOUT = 15           # Could not get a grant to access the volume within defined period
FR_LOCKED = 16            # The operation is rejected according to the file sharing policy
FR_NOT_ENOUGH_CORE = 17   # LFN working buffer could not be allocated
FR_TOO_MANY_OPEN_FILES = 18  # Number of open files > FF_FS_LOCK
FR_INVALID_PARAMETER = 19 # Given parameter is invalid

# File access mode flags
FA_READ = 0x01            # Specifies read access to the object
FA_WRITE = 0x02           # Specifies write access to the object  
FA_OPEN_EXISTING = 0x00   # Opens the file if it exists, fails if it doesn't exist
FA_CREATE_NEW = 0x04      # Creates a new file, fails if file already exists
FA_CREATE_ALWAYS = 0x08   # Creates a new file, truncates if file exists
FA_OPEN_ALWAYS = 0x10     # Opens file if exists, creates new if it doesn't
FA_OPEN_APPEND = 0x30     # Opens file for append (sets pointer to end)

# File attributes
AM_RDO = 0x01    # Read only
AM_HID = 0x02    # Hidden
AM_SYS = 0x04    # System
AM_DIR = 0x10    # Directory
AM_ARC = 0x20    # Archive

def mount(path="/", drive=0, opt=1):
    """
    Mount a filesystem
    
    Args:
        path (str): Mount point path
        drive (int): Drive number
        opt (int): Mount option (0=delayed mount, 1=immediate mount)
    
    Returns:
        int: FatFs result code
    """
    return fatfs.mount(path, drive, opt)

def open_file(path, mode=FA_READ):
    """
    Open a file
    
    Args:
        path (str): File path
        mode (int): Access mode flags
    
    Returns:
        int: File pointer if successful (large number), error code if failed (small number)
    """
    result = fatfs.open(path, mode)
    return result

def close_file(fp):
    """
    Close a file
    
    Args:
        fp: File pointer returned by open_file
    
    Returns:
        int: FatFs result code
    """
    return fatfs.close(fp)

def read_file(fp, size):
    """
    Read data from file
    
    Args:
        fp: File pointer
        size (int): Number of bytes to read
    
    Returns:
        bytes: Data read from file
    """
    return fatfs.read(fp, size)

def write_file(fp, data):
    """
    Write data to file
    
    Args:
        fp: File pointer
        data (bytes or str): Data to write
    
    Returns:
        tuple: (result_code, bytes_written)
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return fatfs.write(fp, data)

def get_error_string(error_code):
    """
    Get human-readable error message for FatFs result code
    
    Args:
        error_code (int): FatFs result code
    
    Returns:
        str: Error message
    """
    error_messages = {
        FR_OK: "Succeeded",
        FR_DISK_ERR: "Hard error occurred in low level disk I/O",
        FR_INT_ERR: "Assertion failed",
        FR_NOT_READY: "Physical drive cannot work",
        FR_NO_FILE: "Could not find the file",
        FR_NO_PATH: "Could not find the path",
        FR_INVALID_NAME: "Path name format is invalid",
        FR_DENIED: "Access denied",
        FR_EXIST: "File already exists",
        FR_INVALID_OBJECT: "File/directory object is invalid",
        FR_WRITE_PROTECTED: "Physical drive is write protected",
        FR_INVALID_DRIVE: "Logical drive number is invalid",
        FR_NOT_ENABLED: "Volume has no work area",
        FR_NO_FILESYSTEM: "No valid FAT volume",
        FR_MKFS_ABORTED: "f_mkfs() aborted",
        FR_TIMEOUT: "Could not get volume access grant",
        FR_LOCKED: "Operation rejected by file sharing policy",
        FR_NOT_ENOUGH_CORE: "LFN working buffer could not be allocated",
        FR_TOO_MANY_OPEN_FILES: "Number of open files exceeded limit",
        FR_INVALID_PARAMETER: "Given parameter is invalid"
    }
    return error_messages.get(error_code, f"Unknown error code: {error_code}")

# Extended file operations
def lseek(fp, offset):
    """
    Move read/write pointer, expand size
    
    Args:
        fp: File pointer
        offset (int): New position
    
    Returns:
        int: FatFs result code
    """
    return fatfs.lseek(fp, offset)

def truncate_file(fp):
    """
    Truncate file size
    
    Args:
        fp: File pointer
    
    Returns:
        int: FatFs result code
    """
    return fatfs.truncate(fp)

def sync_file(fp):
    """
    Flush cached data
    
    Args:
        fp: File pointer
    
    Returns:
        int: FatFs result code
    """
    return fatfs.sync(fp)

def tell(fp):
    """
    Get current read/write pointer
    
    Args:
        fp: File pointer
    
    Returns:
        int: Current position
    """
    return fatfs.tell(fp)

def eof(fp):
    """
    Test for end-of-file
    
    Args:
        fp: File pointer
    
    Returns:
        bool: True if at end of file
    """
    return fatfs.eof(fp)

def file_size(fp):
    """
    Get file size
    
    Args:
        fp: File pointer
    
    Returns:
        int: File size in bytes
    """
    return fatfs.size(fp)

def file_error(fp):
    """
    Test for file error
    
    Args:
        fp: File pointer
    
    Returns:
        bool: True if error occurred
    """
    return fatfs.error(fp)

# Directory operations
def opendir(path):
    """
    Open a directory
    
    Args:
        path (str): Directory path
    
    Returns:
        int: Directory pointer if successful (large number), error code if failed (small number)
    """
    result = fatfs.opendir(path)
    return result

def closedir(dp):
    """
    Close a directory
    
    Args:
        dp: Directory pointer
    
    Returns:
        int: FatFs result code
    """
    return fatfs.closedir(dp)

def readdir(dp):
    """
    Read a directory item
    
    Args:
        dp: Directory pointer
    
    Returns:
        dict or None: File info dict or None if end of directory
    """
    return fatfs.readdir(dp)

# File and directory management
def stat(path):
    """
    Check existence of a file or sub-directory
    
    Args:
        path (str): Path to check
    
    Returns:
        dict: File information dictionary if successful, error code if failed
    """
    result = fatfs.stat(path)
    return result

def unlink(path):
    """
    Remove a file or sub-directory
    
    Args:
        path (str): Path to remove
    
    Returns:
        int: FatFs result code
    """
    return fatfs.unlink(path)

def rename(old_name, new_name):
    """
    Rename/Move a file or sub-directory
    
    Args:
        old_name (str): Current name
        new_name (str): New name
    
    Returns:
        int: FatFs result code
    """
    return fatfs.rename(old_name, new_name)

def chmod(path, attr, mask):
    """
    Change attribute of a file or sub-directory
    
    Args:
        path (str): File path
        attr (int): Attributes to set
        mask (int): Attribute mask
    
    Returns:
        int: FatFs result code
    """
    return fatfs.chmod(path, attr, mask)

def mkdir(path):
    """
    Create a sub-directory
    
    Args:
        path (str): Directory path to create
    
    Returns:
        int: FatFs result code
    """
    return fatfs.mkdir(path)

def chdir(path):
    """
    Change current directory
    
    Args:
        path (str): New current directory
    
    Returns:
        int: FatFs result code
    """
    return fatfs.chdir(path)

def getcwd():
    """
    Retrieve the current directory
    
    Returns:
        str: Current working directory path
    """
    return fatfs.getcwd()

# Volume management
def getfree(path):
    """
    Get free space on the volume
    
    Args:
        path (str): Volume path
    
    Returns:
        dict: Free space information
    """
    return fatfs.getfree(path)

def getlabel(path):
    """
    Get volume label
    
    Args:
        path (str): Volume path
    
    Returns:
        dict: Label and serial number
    """
    return fatfs.getlabel(path)

def setlabel(label):
    """
    Set volume label
    
    Args:
        label (str): New volume label
    
    Returns:
        int: FatFs result code
    """
    return fatfs.setlabel(label)

