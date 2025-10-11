#!/usr/bin/env python3
"""
Test script to verify PyFatFs installation and basic functionality
"""
import sys
import os

def test_import():
    """Test if we can import the modules"""
    print("Testing imports...")
    
    try:
        # Test importing the compiled extension
        import fatfs
        print("[OK] Successfully imported compiled fatfs extension")
        
        # Test importing pyfatfs package
        import pyfatfs
        print("[OK] Successfully imported pyfatfs package")
        
        # Test importing specific modules
        from pyfatfs import core, file
        from pyfatfs.FileAccessWrapper import FatFsFileManager
        print("[OK] Successfully imported pyfatfs modules")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        return False

def test_constants():
    """Test if constants are available"""
    print("\nTesting constants...")
    
    try:
        import pyfatfs
        
        # Test result codes
        assert hasattr(pyfatfs, 'FR_OK')
        assert hasattr(pyfatfs, 'FR_DISK_ERR')
        print("[OK] FatFs result codes available")
        
        # Test file access modes
        assert hasattr(pyfatfs, 'FA_READ')
        assert hasattr(pyfatfs, 'FA_WRITE')
        print("[OK] File access modes available")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Constants test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without actual file operations"""
    print("\nTesting basic functionality...")
    
    try:
        import pyfatfs
        from pyfatfs.FileAccessWrapper import FatFsFileManager
        
        # Test file manager creation
        manager = FatFsFileManager()
        print("[OK] File manager created successfully")
        
        # Test error string function
        error_msg = pyfatfs.get_error_string(pyfatfs.FR_OK)
        assert error_msg == "Succeeded"
        print("[OK] Error string function works")
        
        # Test file object creation (without opening)
        from pyfatfs.file import FatFsFile
        file_obj = FatFsFile("test.txt", "r")
        assert file_obj.path == "test.txt"
        assert file_obj.mode == "r"
        print("[OK] File object creation works")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("PyFatFs Installation and Functionality Test")
    print("=" * 50)
    
    tests = [
        test_import,
        test_constants,
        test_basic_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("[OK] All tests passed! PyFatFs is working correctly.")
        return 0
    else:
        print("[ERROR] Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())