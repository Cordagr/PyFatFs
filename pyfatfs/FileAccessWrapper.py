"""
Enhanced file access wrapper for FatFs
"""
from . import core
from .file import FatFsFile

class FatFsFileManager:
    """File manager for FatFs operations"""
    
    def __init__(self):
        """Initialize the file manager"""
        self.mounted = False
        self.mount_point = "/"
    
    def mount_filesystem(self, path="/", drive=0, opt=1):
        """
        Mount a filesystem
        
        Args:
            path (str): Mount point path
            drive (int): Drive number
            opt (int): Mount option
        
        Returns:
            bool: True if successful
        """
        result = core.mount(path, drive, opt)
        if result == core.FR_OK:
            self.mounted = True
            self.mount_point = path
            return True
        else:
            raise RuntimeError(f"Failed to mount filesystem: {core.get_error_string(result)}")
    
    def is_mounted(self):
        """Check if filesystem is mounted"""
        return self.mounted
    
    def open_file(self, path, mode='r'):
        """
        Open a file with enhanced error handling
        
        Args:
            path (str): File path
            mode (str): File mode
        
        Returns:
            FatFsFile: File object
        """
        if not self.mounted:
            raise RuntimeError("Filesystem not mounted. Call mount_filesystem() first.")
        
        return FatFsFile(path, mode)
    
    def file_exists(self, path):
        """
        Check if file exists (enhanced implementation using stat)
        
        Args:
            path (str): File path
        
        Returns:
            bool: True if file exists
        """
        try:
            result = core.stat(path)
            return isinstance(result, dict)
        except:
            return False
    
    def copy_file(self, src_path, dst_path):
        """
        Copy a file
        
        Args:
            src_path (str): Source file path
            dst_path (str): Destination file path
        
        Returns:
            bool: True if successful
        """
        try:
            with self.open_file(src_path, 'r') as src:
                data = src.read()
                with self.open_file(dst_path, 'w') as dst:
                    dst.write(data)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to copy file: {str(e)}")
    
    def move_file(self, src_path, dst_path):
        """
        Move a file (copy then delete)
        
        Args:
            src_path (str): Source file path
            dst_path (str): Destination file path
        
        Returns:
            bool: True if successful
        """
        self.copy_file(src_path, dst_path)
        self.delete_file(src_path)
        return True
    
    def delete_file(self, path):
        """
        Delete a file
        
        Args:
            path (str): File path
        
        Returns:
            bool: True if successful
        """
        result = core.unlink(path)
        if result != core.FR_OK:
            raise IOError(f"Failed to delete file '{path}': {core.get_error_string(result)}")
        return True
    
    def get_file_size(self, path):
        """
        Get file size using stat
        
        Args:
            path (str): File path
        
        Returns:
            int: File size in bytes
        """
        result = core.stat(path)
        if isinstance(result, int):
            raise IOError(f"Failed to get file size for '{path}': {core.get_error_string(result)}")
        return result['fsize']
    
    def rename_file(self, old_path, new_path):
        """
        Rename/move a file
        
        Args:
            old_path (str): Current file path
            new_path (str): New file path
        
        Returns:
            bool: True if successful
        """
        result = core.rename(old_path, new_path)
        if result != core.FR_OK:
            raise IOError(f"Failed to rename '{old_path}' to '{new_path}': {core.get_error_string(result)}")
        return True
    
    def get_file_info(self, path):
        """
        Get detailed file information
        
        Args:
            path (str): File path
        
        Returns:
            dict: File information including size, date, attributes
        """
        result = core.stat(path)
        if isinstance(result, int) and result < 100:  # Error codes are small integers
            raise IOError(f"Failed to get file info for '{path}': {core.get_error_string(result)}")
        return result
    
    def get_volume_info(self, path="/"):
        """
        Get volume information (free space, etc.)
        
        Args:
            path (str): Volume path
        
        Returns:
            dict: Volume information
        """
        result = core.getfree(path)
        if isinstance(result, int) and result < 100:  # Error codes are small integers
            raise IOError(f"Failed to get volume info: {core.get_error_string(result)}")
        return result


# Global file manager instance
file_manager = FatFsFileManager()

# Convenience functions
def mount(path="/", drive=0, opt=1):
    """Mount filesystem using global file manager"""
    return file_manager.mount_filesystem(path, drive, opt)

def open_file(path, mode='r'):
    """Open file using global file manager"""
    return file_manager.open_file(path, mode)

def file_exists(path):
    """Check if file exists using global file manager"""
    return file_manager.file_exists(path)

def copy_file(src, dst):
    """Copy file using global file manager"""
    return file_manager.copy_file(src, dst)

def move_file(src, dst):
    """Move file using global file manager"""
    return file_manager.move_file(src, dst)

def get_file_size(path):
    """Get file size using global file manager"""
    return file_manager.get_file_size(path)

def delete_file(path):
    """Delete file using global file manager"""
    return file_manager.delete_file(path)

def rename_file(old_path, new_path):
    """Rename file using global file manager"""
    return file_manager.rename_file(old_path, new_path)

def get_file_info(path):
    """Get file info using global file manager"""
    return file_manager.get_file_info(path)

def get_volume_info(path="/"):
    """Get volume info using global file manager"""
    return file_manager.get_volume_info(path)

def is_mounted():
    """Check if filesystem is mounted"""
    return file_manager.is_mounted()
    