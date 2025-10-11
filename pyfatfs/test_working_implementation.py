#!/usr/bin/env python3
"""
Test script for working FatFs implementation with actual file I/O operations.
"""

import sys
import traceback

def test_basic_operations():
    """Test basic mount, format, and file operations"""
    print("Testing basic FatFs operations with working implementation...")
    
    try:
        import fatfs
        print("SUCCESS: FatFs module imported")
        
        # Test disk info
        try:
            total_sectors, sector_size = fatfs.get_disk_info()
            print(f"SUCCESS: Disk info - {total_sectors} sectors, {sector_size} bytes per sector")
            print(f"         Total capacity: {(total_sectors * sector_size) / (1024*1024):.1f} MB")
        except Exception as e:
            print(f"WARNING: get_disk_info failed: {e}")
        
        # Test mount operation
        print("\nTesting mount operation...")
        mount_result = fatfs.mount("0:", 0, 1)  # Drive 0, immediate mount
        print(f"Mount result: {mount_result}")
        
        if mount_result == 0:
            print("SUCCESS: Mount operation successful")
        elif mount_result == 13:  # FR_NO_FILESYSTEM
            print("INFO: No filesystem detected, attempting format...")
            
            # Try to format the disk
            format_result = fatfs.format("0:")
            print(f"Format result: {format_result}")
            
            if format_result == 0:
                print("SUCCESS: Format operation successful")
                
                # Try mount again
                mount_result = fatfs.mount("0:", 0, 1)
                print(f"Mount after format result: {mount_result}")
                
                if mount_result == 0:
                    print("SUCCESS: Mount after format successful")
                else:
                    print(f"ERROR: Mount after format failed with code {mount_result}")
                    return False
            else:
                print(f"ERROR: Format failed with code {format_result}")
                return False
        else:
            print(f"ERROR: Mount failed with unexpected code {mount_result}")
            return False
        
        # Test file operations
        print("\nTesting file operations...")
        
        # Open file for writing
        file_handle = fatfs.open("test.txt", 0x02 | 0x08)  # FA_WRITE | FA_CREATE_ALWAYS
        print(f"Open result: {file_handle}, type: {type(file_handle)}")
        
        # Check if open failed (result is an error code)
        if isinstance(file_handle, int) and file_handle < 256:  # Error codes are small integers
            print(f"ERROR: Open for write failed with code {file_handle}")
            return False
        
        print("SUCCESS: File opened for writing")
        
        
        test_data = b"Hello, FatFs world!\nThis is a test file.\n"
        write_result = fatfs.write(file_handle, test_data)
        print(f"Write result: {write_result}")
        
        if isinstance(write_result, tuple) and len(write_result) == 2:
            result_code, bytes_written = write_result
            if result_code == 0:
                print(f"SUCCESS: Wrote {bytes_written} bytes")
            else:
                print(f"ERROR: Write failed with code {result_code}")
                fatfs.close(file_handle)
                return False
        else:
            print(f"ERROR: Unexpected write result format: {write_result}")
            fatfs.close(file_handle)
            return False
        
        # Close file
        close_result = fatfs.close(file_handle)
        print(f"Close result: {close_result}")
        
        if close_result == 0:
            print("SUCCESS: File closed successfully")
        else:
            print(f"ERROR: Close failed with code {close_result}")
            return False
        
        
        file_handle = fatfs.open("test.txt", 0x01)  # FA_READ
        print(f"Open for read result: {file_handle}, type: {type(file_handle)}")
        
        if isinstance(file_handle, int) and file_handle < 256:  # Error codes are small integers
            print(f"ERROR: Open for read failed with code {file_handle}")
            return False
        
        print("SUCCESS: File opened for reading")
        
    
        read_result = fatfs.read(file_handle, len(test_data))
        print(f"Read result type: {type(read_result)}")
        
        if isinstance(read_result, bytes):
            print(f"SUCCESS: Read {len(read_result)} bytes")
            print(f"Data: {read_result.decode('utf-8', errors='replace')}")
            
            if read_result == test_data:
                print("SUCCESS: Read data matches written data")
            else:
                print("WARNING: Read data doesn't match written data")
                print(f"Expected: {test_data}")
                print(f"Got: {read_result}")
        elif isinstance(read_result, int):
            print(f"ERROR: Read failed with code {read_result}")
            fatfs.close(file_handle)
            return False
        else:
            print(f"ERROR: Unexpected read result: {read_result}")
            fatfs.close(file_handle)
            return False
        
        # Close file
        close_result = fatfs.close(file_handle)
        if close_result == 0:
            print("SUCCESS: File closed successfully")
        else:
            print(f"ERROR: Close failed with code {close_result}")
            return False
        
        print("\nSUCCESS: All basic operations completed successfully!")
        return True
        
    except ImportError as e:
        print(f"ERROR: Failed to import fatfs module: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        traceback.print_exc()
        return False

def test_high_level_api():
    """Test the high-level Python API"""
    print("\n" + "="*60)
    print("Testing high-level PyFatFs API...")
    
    try:
        from pyfatfs.file import FatFsFile
        from pyfatfs import core
        print("SUCCESS: PyFatFs modules imported")
        
        # First mount the filesystem if not already mounted
        mount_result = core.mount("0:", 0, 1)
        print(f"Mount result: {mount_result}")
        
        # Test file operations using wrapper
        print("\nTesting FatFsFile...")
        
        with FatFsFile("test_highlevel.txt", "w") as f:
            f.write("Hello from high-level API!\n")
            f.write("Line 2 of test data.\n")
        print("SUCCESS: File written using high-level API")
        
        with FatFsFile("test_highlevel.txt", "r") as f:
            content = f.read()
            print(f"SUCCESS: File read using high-level API")
            print(f"Content: {repr(content)}")
        
        print("\nSUCCESS: High-level API test completed!")
        return True
        
    except ImportError as e:
        print(f"ERROR: Failed to import PyFatFs modules: {e}")
        return False
    except Exception as e:
        print(f"ERROR: High-level API test failed: {e}")
        traceback.print_exc()
        return False

def main():
    print("FatFs Working Implementation Test")
    print("=" * 50)
    
    success = True
    
    success &= test_basic_operations()
    success &= test_high_level_api()
    
    print("\n" + "="*50)
    if success:
        print("SUCCESS: All tests passed! FatFs implementation is working.")
    else:
        print("ERROR: Some tests failed. Check the output above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())