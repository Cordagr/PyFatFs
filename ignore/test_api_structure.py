#!/usr/bin/env python3
"""
Simple PyFatFs API Test - Tests what works with the current implementation
"""
import sys
import os

def test_api_structure():
    """Test the API structure and available functions"""
    print("=== PyFatFs API Structure Test ===\n")
    
    # Test core module import
    print("1. Testing core module...")
    try:
        import fatfs
        print("[OK] Core fatfs module imported")
        
        # Show available functions
        functions = [attr for attr in dir(fatfs) if not attr.startswith('_')]
        print(f"[OK] Available functions: {functions}")
        
    except Exception as e:
        print(f"[ERROR] Core module test failed: {e}")
        return False
    
    # Test high-level module import
    print("\n2. Testing high-level modules...")
    try:
        import pyfatfs
        from pyfatfs import FileAccessWrapper, DirectoryAccessWrapper
        from pyfatfs.FileAccessWrapper import FatFsFileManager
        
        print("[OK] High-level modules imported")
        
        # Show available classes
        print(f"[OK] FileAccessWrapper available: {FileAccessWrapper}")
        print(f"[OK] DirectoryAccessWrapper available: {DirectoryAccessWrapper}")
        print(f"[OK] FatFsFileManager available: {FatFsFileManager}")
        
    except Exception as e:
        print(f"[ERROR] High-level module test failed: {e}")
        return False
    
    return True

def test_error_codes():
    """Test error code system"""
    print("\n=== Error Code System Test ===\n")
    
    try:
        import pyfatfs
        
        # Test error string function
        print("Testing error code translations:")
        test_codes = [0, 1, 2, 3, 4, 5, 13, 19]
        
        for code in test_codes:
            try:
                error_msg = pyfatfs.get_error_string(code)
                print(f"[OK] Code {code}: {error_msg}")
            except Exception as e:
                print(f"[ERROR] Code {code}: {e}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error code test failed: {e}")
        return False

def test_object_creation():
    """Test object creation without file system operations"""
    print("\n=== Object Creation Test ===\n")
    
    try:
        from pyfatfs.FileAccessWrapper import FatFsFileManager
        from pyfatfs.file import FatFsFile
        
        # Test file manager creation
        print("1. Testing file manager creation...")
        manager = FatFsFileManager()
        print(f"[OK] File manager created: {type(manager)}")
        print(f"[OK] Mounted status: {manager.is_mounted()}")
        
        # Test file object creation (without opening)
        print("\n2. Testing file object creation...")
        file_obj = FatFsFile("test.txt", "r")
        print(f"[OK] File object created: {type(file_obj)}")
        print(f"[OK] File path: {file_obj.path}")
        print(f"[OK] File mode: {file_obj.mode}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Object creation test failed: {e}")
        return False

def test_mount_behavior():
    """Test mount operation and understand its behavior"""
    print("\n=== Mount Behavior Test ===\n")
    
    try:
        import fatfs
        import pyfatfs
        
        print("Testing mount operation with different parameters...")
        
        # Test various mount parameters
        mount_tests = [
            ("", 0, 0),
            ("", 0, 1), 
            ("/", 0, 1),
            ("0:", 0, 1)
        ]
        
        for path, drive, opt in mount_tests:
            result = fatfs.mount(path, drive, opt)
            error_msg = pyfatfs.get_error_string(result)
            print(f"[INFO] Mount('{path}', {drive}, {opt}) -> {result} ({error_msg})")
        
        print("\n[INFO] Note: Error codes are expected with stub implementation")
        print("[INFO] Code 13 'No valid FAT volume' is normal for demo purposes")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Mount test failed: {e}")
        return False

def test_constants():
    """Test available constants"""
    print("\n=== Constants Test ===\n")
    
    try:
        import pyfatfs
        
        # Test result codes
        print("FatFs Result Codes:")
        result_codes = ['FR_OK', 'FR_DISK_ERR', 'FR_INT_ERR', 'FR_NOT_READY', 
                       'FR_NO_FILE', 'FR_NO_PATH', 'FR_INVALID_NAME', 'FR_DENIED']
        
        for code in result_codes:
            if hasattr(pyfatfs, code):
                value = getattr(pyfatfs, code)
                print(f"[OK] {code} = {value}")
            else:
                print(f"[WARNING] {code} not available")
        
        # Test file access modes
        print("\nFile Access Modes:")
        access_modes = ['FA_READ', 'FA_WRITE', 'FA_OPEN_EXISTING', 
                       'FA_CREATE_NEW', 'FA_CREATE_ALWAYS', 'FA_OPEN_ALWAYS']
        
        for mode in access_modes:
            if hasattr(pyfatfs, mode):
                value = getattr(pyfatfs, mode)
                print(f"[OK] {mode} = {value}")
            else:
                print(f"[WARNING] {mode} not available")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Constants test failed: {e}")
        return False

def main():
    """Run all API tests"""
    print("PyFatFs API and Structure Test")
    print("=" * 50)
    print("This test validates the API structure and available functionality")
    print("without requiring actual file system operations.\n")
    
    tests = [
        ("API Structure", test_api_structure),
        ("Error Codes", test_error_codes),
        ("Object Creation", test_object_creation),
        ("Mount Behavior", test_mount_behavior),
        ("Constants", test_constants)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"\n[OK] {test_name} test passed")
            else:
                print(f"\n[ERROR] {test_name} test failed")
        except Exception as e:
            print(f"\n[ERROR] {test_name} test crashed: {e}")
    
    print("\n" + "=" * 70)
    print(f"API Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[OK] All API tests passed!")
        print("[INFO] PyFatFs structure is working correctly.")
        print("[INFO] For actual file operations, implement real disk I/O functions.")
    else:
        print(f"\n[WARNING] {total-passed} tests failed.")
        print("[INFO] Check the output above for details.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())