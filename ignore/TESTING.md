# PyFatFs Testing Guide

This guide covers how to test the PyFatFs implementation at different levels.

## Prerequisites

Before testing, ensure you have:
- Built the PyFatFs extension: `python setup.py build_ext --inplace`
- Python 3.6+ installed
- The fatfs.cp312-win_amd64.pyd file in your project directory

## Test Levels

### Level 1: Installation and Import Tests

Test that the modules can be imported and basic functionality works:

```bash
python test_installation.py
```

**Expected Output:**
```
PyFatFs Installation and Functionality Test
==================================================
Testing imports...
[OK] Successfully imported compiled fatfs extension
[OK] Successfully imported pyfatfs package
[OK] Successfully imported pyfatfs modules

Testing constants...
[OK] FatFs result codes available
[OK] File access modes available

Testing basic functionality...
[OK] File manager created successfully
[OK] Error string function works
[OK] File object creation works

==================================================
Test Results: 3/3 tests passed
[OK] All tests passed! PyFatFs is working correctly.
```

### Level 2: Error Code Testing

Test the error handling and result codes:

```python
import fatfs
import pyfatfs

# Test mount with various parameters
result = fatfs.mount("", 0, 1)
print(f"Mount result: {result}")
print(f"Error meaning: {pyfatfs.get_error_string(result)}")

# Common result codes:
# 0  = FR_OK (Success)
# 1  = FR_DISK_ERR (Disk error)
# 13 = FR_NO_FILESYSTEM (No valid filesystem)
# 19 = FR_INVALID_DRIVE (Invalid drive)
```

### Level 3: File Manager Testing

Test the file manager functionality:

```bash
python examples\file_manager_demo.py
```

### Level 4: Comprehensive Functionality Tests

Run the comprehensive demos to test various features:

#### File Operations Demo
```bash
python examples\comprehensive_file_operations.py
```

Tests:
- File creation (text and binary)
- Reading files (full and chunked)
- File positioning and seeking
- Append operations
- Large file handling
- Error scenarios

#### Directory Management Demo
```bash
python examples\advanced_directory_management.py
```

Tests:
- Directory creation and listing
- Recursive traversal
- Directory statistics
- Path validation

#### Performance Benchmarking
```bash
python examples\performance_benchmarking.py
```

Tests:
- File creation performance
- Read/write speed with different buffer sizes
- Sequential vs random access
- Memory usage patterns

#### Error Handling Demo
```bash
python examples\error_handling.py
```

Tests:
- File not found scenarios
- Permission errors
- Invalid operations
- Recovery mechanisms

## Understanding Test Results

### Successful Tests
- `[OK]` messages indicate successful operations
- Return code `0` from scripts means success
- No exceptions thrown during operations

### Common Issues and Solutions

#### Mount Errors
```
Mount result: 13
Error meaning: No valid file system
```

**Solutions:**
1. **Expected Behavior**: This is normal for the demo implementation as we don't have a real storage device
2. **For Real Hardware**: You need to implement proper disk I/O functions in `diskio.c`
3. **For Testing**: The stub implementation allows testing of API structure

#### Import Errors
```
ImportError: No module named 'fatfs'
```

**Solutions:**
1. Rebuild the extension: `python setup.py build_ext --inplace`
2. Check if `fatfs.cp312-win_amd64.pyd` exists in the directory
3. Verify Python version compatibility

#### File Operation Errors
```
Error: Failed to open file 'test.txt': Assertion failed
```

**Solutions:**
1. **Expected in Demo**: The minimal disk I/O implementation is a stub
2. **For Real Use**: Implement actual storage operations in `diskio_minimal.c`
3. **Testing APIs**: Focus on testing the Python bindings rather than actual file I/O

## Test Categories

### Unit Tests (test_installation.py)
- ✅ Module imports
- ✅ Constant definitions
- ✅ Basic object creation
- ✅ Error string functions

### Integration Tests (examples/)
- ⚠️ File operations (limited by stub implementation)
- ⚠️ Directory operations (limited by stub implementation)
- ✅ Error handling patterns
- ✅ Performance measurement structure

### API Tests
- ✅ Python C extension interface
- ✅ High-level wrapper classes
- ✅ Context managers
- ✅ Exception handling

## Manual Testing

### Test the Core Extension
```python
import fatfs

# Test low-level functions
print("Testing core fatfs functions:")
result = fatfs.mount("", 0, 1)
print(f"Mount: {result}")

# Test file operations (will fail with stub implementation)
try:
    file_handle = fatfs.open("test.txt", 1)  # FA_CREATE_NEW
    print(f"File handle: {file_handle}")
except Exception as e:
    print(f"Expected error: {e}")
```

### Test High-Level Wrappers
```python
from pyfatfs import FileAccessWrapper, DirectoryAccessWrapper

# Test file wrapper creation
try:
    file_wrapper = FileAccessWrapper("test.txt", "w")
    print("File wrapper created successfully")
except Exception as e:
    print(f"Error: {e}")

# Test directory wrapper creation
try:
    dir_wrapper = DirectoryAccessWrapper("test_dir")
    print("Directory wrapper created successfully")
except Exception as e:
    print(f"Error: {e}")
```

## Expected Test Outcomes

### With Stub Implementation (Current State)
- ✅ Module imports work
- ✅ Object creation works
- ✅ Error handling works
- ⚠️ Actual file I/O operations fail (expected)
- ✅ API structure is validated

### With Real Implementation (Production)
- ✅ All of the above
- ✅ Actual file I/O operations work
- ✅ Real filesystem operations
- ✅ Hardware integration

## Development Testing Workflow

1. **Start with**: `python test_installation.py`
2. **Then run**: `python examples\file_manager_demo.py`
3. **Debug issues** using error codes and messages
4. **Test specific features** with individual example scripts
5. **Performance test** with `python examples\performance_benchmarking.py`

## Troubleshooting

### Build Issues
```bash
# Clean and rebuild
python setup.py clean --all
python setup.py build_ext --inplace
```

### Runtime Issues
```python
# Check available functions
import fatfs
print(dir(fatfs))

# Check error meanings
import pyfatfs
for i in range(20):
    print(f"{i}: {pyfatfs.get_error_string(i)}")
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Your test code here
```

## Test Automation

Create a test runner script:

```python
import subprocess
import sys

tests = [
    "test_installation.py",
    "examples/file_manager_demo.py",
    "examples/error_handling.py"
]

for test in tests:
    print(f"\n=== Running {test} ===")
    result = subprocess.run([sys.executable, test], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
```

This testing approach validates the PyFatFs implementation structure and API design, even when working with a minimal stub implementation for the underlying file operations.