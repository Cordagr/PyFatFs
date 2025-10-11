#!/usr/bin/env python3
"""
Example: Basic file operations with PyFatFs
"""
import sys
import os

# Add parent directory to path to import pyfatfs
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyfatfs

def main():
    """Demonstrate basic file operations"""
    
    try:
        # Mount the filesystem
        print("Mounting filesystem...")
        result = pyfatfs.mount("/", 0, 1)
        print(f"Mount result: {result}")
        
        # Create and write a file
        print("\nCreating and writing to a file...")
        with pyfatfs.open_file("test.txt", "w") as f:
            bytes_written = f.write("Hello, FatFs World!\nThis is a test file.\n")
            print(f"Written {bytes_written} bytes")
        
        # Read the file back
        print("\nReading file content...")
        with pyfatfs.open_file("test.txt", "r") as f:
            content = f.read()
            print(f"File content:\n{content.decode() if isinstance(content, bytes) else content}")
        
        # Append to the file
        print("\nAppending to file...")
        with pyfatfs.open_file("test.txt", "a") as f:
            bytes_written = f.write("Appended line.\n")
            print(f"Appended {bytes_written} bytes")
        
        # Read the updated file
        print("\nReading updated file content...")
        with pyfatfs.open_file("test.txt", "r") as f:
            content = f.read()
            print(f"Updated content:\n{content.decode() if isinstance(content, bytes) else content}")
            
        print("\nFile operations completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())