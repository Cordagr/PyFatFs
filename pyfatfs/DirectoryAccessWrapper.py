"""
Directory access wrapper for FatFs Python bindings
Provides high-level directory operations with error handling
"""

from . import core

class FatFsDirectory:
    """Directory object with context manager support"""
    
    def __init__(self, path):
        self.path = path
        self.dp = None
        self.is_open = False
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def open(self):
        """Open the directory"""
        if self.is_open:
            raise ValueError("Directory already open")
        
        result = core.opendir(self.path)
        if isinstance(result, int) and result < 100:  # Error codes are small integers
            # Error occurred
            error_msg = core.get_error_string(result)
            raise IOError(f"Failed to open directory '{self.path}': {error_msg}")
        
        self.dp = result
        self.is_open = True
    
    def close(self):
        """Close the directory"""
        if not self.is_open:
            return
        
        if self.dp:
            core.closedir(self.dp)
            self.dp = None
        self.is_open = False
    
    def read(self):
        """Read next directory entry"""
        if not self.is_open:
            raise ValueError("Directory not open")
        
        result = core.readdir(self.dp)
        if isinstance(result, int) and result < 100:  # Error codes are small integers
            # Error occurred
            error_msg = core.get_error_string(result)
            raise IOError(f"Failed to read directory: {error_msg}")
        
        return result  # None if end of directory, dict if valid entry
    
    def list_all(self):
        """List all entries in directory"""
        entries = []
        while True:
            entry = self.read()
            if entry is None:
                break
            entries.append(entry)
        return entries

class FatFsDirectoryManager:
    """High-level directory management operations"""
    
    @staticmethod
    def list_directory(path):
        """
        List all files and directories in the given path
        
        Args:
            path (str): Directory path to list
        
        Returns:
            list: List of file/directory info dictionaries
        """
        with FatFsDirectory(path) as directory:
            return directory.list_all()
    
    @staticmethod
    def create_directory(path):
        """
        Create a new directory
        
        Args:
            path (str): Directory path to create
        
        Returns:
            bool: True if successful
        
        Raises:
            IOError: If creation fails
        """
        result = core.mkdir(path)
        if result != core.FR_OK:
            error_msg = core.get_error_string(result)
            raise IOError(f"Failed to create directory '{path}': {error_msg}")
        return True
    
    @staticmethod
    def remove_directory(path):
        """
        Remove a directory (must be empty)
        
        Args:
            path (str): Directory path to remove
        
        Returns:
            bool: True if successful
        
        Raises:
            IOError: If removal fails
        """
        result = core.unlink(path)
        if result != core.FR_OK:
            error_msg = core.get_error_string(result)
            raise IOError(f"Failed to remove directory '{path}': {error_msg}")
        return True
    
    @staticmethod
    def change_directory(path):
        """
        Change current working directory
        
        Args:
            path (str): New working directory
        
        Returns:
            bool: True if successful
        
        Raises:
            IOError: If change fails
        """
        result = core.chdir(path)
        if result != core.FR_OK:
            error_msg = core.get_error_string(result)
            raise IOError(f"Failed to change directory to '{path}': {error_msg}")
        return True
    
    @staticmethod
    def get_current_directory():
        """
        Get current working directory
        
        Returns:
            str: Current working directory path
        
        Raises:
            IOError: If operation fails
        """
        result = core.getcwd()
        if isinstance(result, int):
            error_msg = core.get_error_string(result)
            raise IOError(f"Failed to get current directory: {error_msg}")
        return result
    
    @staticmethod
    def file_exists(path):
        """
        Check if a file or directory exists
        
        Args:
            path (str): Path to check
        
        Returns:
            bool: True if exists
        """
        try:
            result = core.stat(path)
            return isinstance(result, dict) or (isinstance(result, int) and result >= 100)
        except:
            return False
    
    @staticmethod
    def get_file_info(path):
        """
        Get detailed information about a file or directory
        
        Args:
            path (str): Path to check
        
        Returns:
            dict: File information
        
        Raises:
            IOError: If file doesn't exist or operation fails
        """
        result = core.stat(path)
        if isinstance(result, int) and result < 100:  # Error codes are small integers
            error_msg = core.get_error_string(result)
            raise IOError(f"Failed to get info for '{path}': {error_msg}")
        return result
    
    @staticmethod
    def is_directory(path):
        """
        Check if path is a directory
        
        Args:
            path (str): Path to check
        
        Returns:
            bool: True if it's a directory
        """
        try:
            info = FatFsDirectoryManager.get_file_info(path)
            return bool(info['fattrib'] & core.AM_DIR)
        except:
            return False
    
    @staticmethod
    def is_file(path):
        """
        Check if path is a file (not directory)
        
        Args:
            path (str): Path to check
        
        Returns:
            bool: True if it's a file
        """
        try:
            info = FatFsDirectoryManager.get_file_info(path)
            return not bool(info['fattrib'] & core.AM_DIR)
        except:
            return False
    
    @staticmethod
    def rename_file(old_path, new_path):
        """
        Rename or move a file/directory
        
        Args:
            old_path (str): Current path
            new_path (str): New path
        
        Returns:
            bool: True if successful
        
        Raises:
            IOError: If operation fails
        """
        result = core.rename(old_path, new_path)
        if result != core.FR_OK:
            error_msg = core.get_error_string(result)
            raise IOError(f"Failed to rename '{old_path}' to '{new_path}': {error_msg}")
        return True
    
    @staticmethod
    def delete_file(path):
        """
        Delete a file
        
        Args:
            path (str): File path to delete
        
        Returns:
            bool: True if successful
        
        Raises:
            IOError: If deletion fails
        """
        result = core.unlink(path)
        if result != core.FR_OK:
            error_msg = core.get_error_string(result)
            raise IOError(f"Failed to delete file '{path}': {error_msg}")
        return True

def open_directory(path):
    """
    Open a directory with context manager support
    
    Args:
        path (str): Directory path
    
    Returns:
        FatFsDirectory: Directory object
    """
    return FatFsDirectory(path)


def create_directory(path):
    """
    Create a directory
    
    Args:
        path (str): Directory path
    
    Returns:
        bool: True if successful
    """
    directory = FatFsDirectory(path)
    directory.create()
    return True

def list_directory(path):
    """
    List contents of a directory
    
    Args:
        path (str): Directory path
    
    Returns:
        list: List of items in directory
    """
    directory = FatFsDirectory(path)
    return directory.list_files()

def remove_directory(path):
    """
    Remove a directory
    
    Args:
        path (str): Directory path
    
    Returns:
        bool: True if successful
    """
    directory = FatFsDirectory(path)
    directory.remove()
    return True

def directory_exists(path):
    """
    Check if directory exists
    
    Args:
        path (str): Directory path
    
    Returns:
        bool: True if directory exists
    """
    directory = FatFsDirectory(path)
    return directory.exists()

# Utility functions for path operations
def join_path(*parts):
    """Join path components"""
    return "/".join(parts)

def normalize_path(path):
    """Normalize path for FatFs"""
    return path.replace("\\", "/")

def get_parent_path(path):
    """Get parent directory path"""
    normalized = normalize_path(path)
    return "/".join(normalized.split("/")[:-1]) or "/"

def get_filename(path):
    """Get filename from path"""
    normalized = normalize_path(path)
    return normalized.split("/")[-1]
    