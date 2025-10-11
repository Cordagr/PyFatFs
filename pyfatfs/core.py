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
        int or file pointer: File pointer if successful, error code if failed
    """
    return fatfs.open(path, mode)

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

