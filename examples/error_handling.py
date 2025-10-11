#!/usr/bin/env python3
"""
Example: Error handling with PyFatFs
"""
import sys
import os

# Add parent directory to path to import pyfatfs
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyfatfs

def main():
    """Demonstrate error handling"""
    
    try:
        # Mount filesystem
        print("Mounting filesystem...")
        result = pyfatfs.mount("/", 0, 1)
        
        if result != pyfatfs.FR_OK:
            print(f"Mount failed: {pyfatfs.get_error_string(result)}")
            return 1
        
        print("Filesystem mounted successfully!")
        
        # Try to open a non-existent file
        print("\nTrying to open non-existent file...")
        try:
            with pyfatfs.open_file("nonexistent.txt", "r") as f:
                content = f.read()
        except IOError as e:
            print(f"Expected error caught: {e}")
        
        # Try invalid file mode
        print("\nTrying invalid operations...")
        try:
            with pyfatfs.open_file("test.txt", "w") as f:
                f.write("Test content")
            
            # Try to write to read-only file
            with pyfatfs.open_file("test.txt", "r") as f:
                f.write("This should fail")
                
        except Exception as e:
            print(f"Expected error caught: {e}")
        
        # Demonstrate proper error handling
        print("\nDemonstrating proper error handling...")
        
        filename = "error_test.txt"
        try:
            # Create file
            with pyfatfs.open_file(filename, "w") as f:
                f.write("Content for error testing\n")
            print(f"Created {filename} successfully")
            
            # Read it back
            with pyfatfs.open_file(filename, "r") as f:
                content = f.read()
                print(f"Read content: {content.decode() if isinstance(content, bytes) else content}")
                
        except IOError as e:
            print(f"IO Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        print("\nError handling demonstration completed!")
        
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())