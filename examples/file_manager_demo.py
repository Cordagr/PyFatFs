#!/usr/bin/env python3
"""
Example: File manager usage with PyFatFs
"""
import sys
import os

# Add parent directory to path to import pyfatfs
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyfatfs.FileAccessWrapper import FatFsFileManager

def main():
    """Demonstrate file manager usage"""
    
    # Create a file manager instance
    file_manager = FatFsFileManager()
    
    try:
        # Mount filesystem
        print("Mounting filesystem...")
        file_manager.mount_filesystem("/", 0, 1)
        print("Filesystem mounted successfully!")
        
        # Check if mounted
        print(f"Is mounted: {file_manager.is_mounted()}")
        
        # Create a test file
        test_file = "manager_test.txt"
        print(f"\nCreating file: {test_file}")
        
        with file_manager.open_file(test_file, "w") as f:
            f.write("File created with FatFsFileManager\n")
            f.write("Multiple lines of text\n")
            f.write("End of file\n")
        
    
        print(f"File exists: {file_manager.file_exists(test_file)}")
        
       
        size = file_manager.get_file_size(test_file)
        print(f"File size: {size} bytes")
        
        # Read file content
        print(f"\nReading file content:")
        with file_manager.open_file(test_file, "r") as f:
            content = f.read()
            print(content.decode() if isinstance(content, bytes) else content)
        
        # Copy the file
        copy_file = "manager_test_copy.txt"
        print(f"\nCopying {test_file} to {copy_file}")
        file_manager.copy_file(test_file, copy_file)
        print("File copied successfully!")
        
        # Verify copy exists
        print(f"Copy exists: {file_manager.file_exists(copy_file)}")
        
        print("\nFile manager operations completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())