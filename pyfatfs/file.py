"""
High-level file operations using FatFs
"""
from . import core

class FatFsFile:
    """High-level file interface for FatFs"""
    
    def __init__(self, path, mode='r'):
        """
        Initialize a FatFs file object
        
        Args:
            path (str): File path
            mode (str): File mode ('r', 'w', 'a', 'r+', 'w+')
        """
        self.path = path
        self.mode = mode
        self.fp = None
        self.is_open = False
        
        # Convert Python mode to FatFs flags
        self.access_mode = self._convert_mode(mode)
    
    def _convert_mode(self, mode):
        """Convert Python file mode to FatFs access flags"""
        mode_map = {
            'r': core.FA_READ | core.FA_OPEN_EXISTING,
            'w': core.FA_WRITE | core.FA_CREATE_ALWAYS,
            'a': core.FA_WRITE | core.FA_OPEN_ALWAYS | core.FA_OPEN_APPEND,
            'r+': core.FA_READ | core.FA_WRITE | core.FA_OPEN_EXISTING,
            'w+': core.FA_READ | core.FA_WRITE | core.FA_CREATE_ALWAYS,
            'a+': core.FA_READ | core.FA_WRITE | core.FA_OPEN_ALWAYS | core.FA_OPEN_APPEND
        }
        return mode_map.get(mode, core.FA_READ | core.FA_OPEN_EXISTING)
    
    def open(self):
        """Open the file"""
        if self.is_open:
            return True
            
        result = core.open_file(self.path, self.access_mode)
        
        # Check if result is an error code (small integer) or valid file pointer (large integer)
        if isinstance(result, int):
            if result < 256:  # Error codes are small integers
                raise IOError(f"Failed to open file '{self.path}': {core.get_error_string(result)}")
            else:  # Large integer is a valid file pointer
                self.fp = result
                self.is_open = True
                return True
        else:
            raise IOError(f"Unexpected open result: {result}")
    
    def close(self):
        """Close the file"""
        if not self.is_open or self.fp is None:
            return
            
        result = core.close_file(self.fp)
        if result != core.FR_OK:
            raise IOError(f"Failed to close file: {core.get_error_string(result)}")
        
        self.fp = None
        self.is_open = False
    
    def read(self, size=-1):
        """
        Read data from file
        
        Args:
            size (int): Number of bytes to read (-1 for all)
        
        Returns:
            bytes: Data read from file
        """
        if not self.is_open:
            raise ValueError("File is not open")
        
        if size == -1:
            size = 1024 * 1024  # Default to 1MB max
        
        try:
            data = core.read_file(self.fp, size)
            if isinstance(data, int):
                # Error code returned
                raise IOError(f"Failed to read from file: {core.get_error_string(data)}")
            return data
        except Exception as e:
            raise IOError(f"Failed to read from file: {str(e)}")
    
    def write(self, data):
        """
        Write data to file
        
        Args:
            data (str or bytes): Data to write
        
        Returns:
            int: Number of bytes written
        """
        if not self.is_open:
            raise ValueError("File is not open")
        
        try:
            result = core.write_file(self.fp, data)
            if isinstance(result, tuple) and len(result) == 2:
                error_code, bytes_written = result
                if error_code != core.FR_OK:
                    raise IOError(f"Write failed: {core.get_error_string(error_code)}")
                return bytes_written
            else:
                raise IOError(f"Unexpected write result format: {result}")
        except Exception as e:
            raise IOError(f"Failed to write to file: {str(e)}")
    
    def __enter__(self):
        """Context manager entry"""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def open_file(path, mode='r'):
    """
    Open a file with FatFs
    
    Args:
        path (str): File path
        mode (str): File mode
    
    Returns:
        FatFsFile: File object
    """
    return FatFsFile(path, mode)

def read_file_content(path):
    """
    Read entire file content
    
    Args:
        path (str): File path
    
    Returns:
        bytes: File content
    """
    with open_file(path, 'r') as f:
        return f.read()

def write_file_content(path, data):
    """
    Write data to file (overwrites existing)
    
    Args:
        path (str): File path
        data (str or bytes): Data to write
    
    Returns:
        int: Number of bytes written
    """
    with open_file(path, 'w') as f:
        return f.write(data)

def append_file_content(path, data):
    """
    Append data to file
    
    Args:
        path (str): File path
        data (str or bytes): Data to append
    
    Returns:
        int: Number of bytes written
    """
    with open_file(path, 'a') as f:
        return f.write(data)
