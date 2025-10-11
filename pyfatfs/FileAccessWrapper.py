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
        Check if file exists (basic implementation)
        
        Args:
            path (str): File path
        
        Returns:
            bool: True if file exists
        """
        try:
            with self.open_file(path, 'r') as f:
                return True
        except (IOError, OSError):
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
        Delete a file (placeholder implementation)
        
        Args:
            path (str): File path
        
        Returns:
            bool: True if successful
        """
        
        raise NotImplementedError("File deletion requires f_unlink implementation in C extension")
    
    def get_file_size(self, path):
        """
        Get file size
        
        Args:
            path (str): File path
        
        Returns:
            int: File size in bytes
        """
        try:
            with self.open_file(path, 'r') as f:
                data = f.read()
                return len(data)
        except Exception as e:
            raise RuntimeError(f"Failed to get file size: {str(e)}")


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

def is_mounted():
    """Check if filesystem is mounted"""
    return file_manager.is_mounted()
    