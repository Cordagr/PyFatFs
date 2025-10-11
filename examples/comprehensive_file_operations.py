#!/usr/bin/env python3
"""
Comprehensive File Operations Demo for PyFatFs

This demo shows advanced file operations including:
- Creating and writing files with different modes
- Reading files in chunks and lines
- File positioning and seeking
- File metadata and attributes
- Binary vs text file handling
- Error handling and recovery
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyfatfs import FileAccessWrapper
import fatfs

def demonstrate_file_creation():
    """Demo creating files with different write modes"""
    print("=== File Creation Demo ===")
    
    # Create a new file with text content
    print("1. Creating a text file...")
    try:
        file_wrapper = FileAccessWrapper("demo_text.txt", "w")
        content = """This is a demonstration file for PyFatFs.
It contains multiple lines of text.
Each line demonstrates different capabilities.
Line 4: Numbers 12345
Line 5: Special chars !@#$%^&*()
"""
        file_wrapper.write(content)
        file_wrapper.close()
        print("   [OK] Text file created successfully")
    except Exception as e:
        print(f"   [ERROR] Error creating text file: {e}")
    
    # Create a binary file
    print("2. Creating a binary file...")
    try:
        file_wrapper = FileAccessWrapper("demo_binary.bin", "wb")
        # Write binary data (example: a simple bitmap-like pattern)
        binary_data = bytes(range(256))  # 0-255 byte values
        file_wrapper.write(binary_data)
        file_wrapper.close()
        print("   [OK] Binary file created successfully")
    except Exception as e:
        print(f"   [ERROR] Error creating binary file: {e}")

def demonstrate_file_reading():
    """Demo different file reading methods"""
    print("\n=== File Reading Demo ===")
    
    # Read entire file at once
    print("1. Reading entire text file...")
    try:
        file_wrapper = FileAccessWrapper("demo_text.txt", "r")
        content = file_wrapper.read()
        print(f"   File size: {len(content)} characters")
        print(f"   First 50 chars: {repr(content[:50])}")
        file_wrapper.close()
        print("   [OK] Full file read successfully")
    except Exception as e:
        print(f"   [ERROR] Error reading file: {e}")
    
    # Read file in chunks
    print("2. Reading file in 32-byte chunks...")
    try:
        file_wrapper = FileAccessWrapper("demo_text.txt", "r")
        chunk_size = 32
        chunk_count = 0
        while True:
            chunk = file_wrapper.read(chunk_size)
            if not chunk:
                break
            chunk_count += 1
            print(f"   Chunk {chunk_count}: {repr(chunk[:20])}...")
            if chunk_count >= 3:  # Limit output
                print("   ... (remaining chunks)")
                break
        file_wrapper.close()
        print("   [OK] Chunked reading completed")
    except Exception as e:
        print(f"   [ERROR] Error reading chunks: {e}")
    
    # Read binary file
    print("3. Reading binary file...")
    try:
        file_wrapper = FileAccessWrapper("demo_binary.bin", "rb")
        binary_data = file_wrapper.read(16)  # Read first 16 bytes
        print(f"   First 16 bytes: {[hex(b) for b in binary_data]}")
        file_wrapper.close()
        print("   [OK] Binary file read successfully")
    except Exception as e:
        print(f"   [ERROR] Error reading binary file: {e}")

def demonstrate_file_positioning():
    """Demo file seeking and positioning"""
    print("\n=== File Positioning Demo ===")
    
    try:
        file_wrapper = FileAccessWrapper("demo_text.txt", "r")
        
        # Read from beginning
        print("1. Reading from beginning...")
        start_content = file_wrapper.read(20)
        print(f"   Content: {repr(start_content)}")
        
        # Seek to middle and read
        print("2. Seeking to position 50...")
        file_wrapper.seek(50)
        middle_content = file_wrapper.read(20)
        print(f"   Content: {repr(middle_content)}")
        
        # Seek to end and get position
        print("3. Seeking to end...")
        file_wrapper.seek(0, 2)  # Seek to end
        file_size = file_wrapper.tell()
        print(f"   File size: {file_size} bytes")
        
        # Seek back and read
        print("4. Seeking back 30 bytes from end...")
        file_wrapper.seek(-30, 2)
        end_content = file_wrapper.read()
        print(f"   Content: {repr(end_content)}")
        
        file_wrapper.close()
        print("   [OK] File positioning demo completed")
    except Exception as e:
        print(f"   [ERROR] Error in file positioning: {e}")

def demonstrate_append_operations():
    """Demo appending to existing files"""
    print("\n=== File Append Demo ===")
    
    # Create initial file
    print("1. Creating initial file...")
    try:
        file_wrapper = FileAccessWrapper("demo_append.txt", "w")
        file_wrapper.write("Initial content\n")
        file_wrapper.close()
        print("   [OK] Initial file created")
    except Exception as e:
        print(f"   [ERROR] Error creating initial file: {e}")
        return
    
    # Append to file multiple times
    print("2. Appending content multiple times...")
    for i in range(3):
        try:
            file_wrapper = FileAccessWrapper("demo_append.txt", "a")
            file_wrapper.write(f"Appended line {i+1}\n")
            file_wrapper.close()
            print(f"   [OK] Append {i+1} completed")
        except Exception as e:
            print(f"   [ERROR] Error in append {i+1}: {e}")
    
    # Read final result
    print("3. Reading final file content...")
    try:
        file_wrapper = FileAccessWrapper("demo_append.txt", "r")
        content = file_wrapper.read()
        print("   Final content:")
        for line_num, line in enumerate(content.splitlines(), 1):
            print(f"   Line {line_num}: {line}")
        file_wrapper.close()
    except Exception as e:
        print(f"   [ERROR] Error reading final content: {e}")

def demonstrate_large_file_operations():
    """Demo handling larger files efficiently"""
    print("\n=== Large File Operations Demo ===")
    
    # Create a larger file
    print("1. Creating a large file (1MB)...")
    try:
        file_wrapper = FileAccessWrapper("demo_large.txt", "w")
        
        # Write 1MB of structured data
        for block in range(1024):  # 1024 blocks
            line = f"Block {block:04d}: " + "A" * 1000 + "\n"  # ~1KB per line
            file_wrapper.write(line)
        
        file_wrapper.close()
        print("   [OK] Large file created (1MB)")
    except Exception as e:
        print(f"   [ERROR] Error creating large file: {e}")
        return
    
    # Read large file efficiently
    print("2. Reading large file in chunks...")
    try:
        file_wrapper = FileAccessWrapper("demo_large.txt", "r")
        chunk_size = 8192  # 8KB chunks
        total_read = 0
        chunk_count = 0
        
        while True:
            chunk = file_wrapper.read(chunk_size)
            if not chunk:
                break
            total_read += len(chunk)
            chunk_count += 1
            
            if chunk_count % 32 == 0:  # Progress every 256KB
                print(f"   Progress: {total_read/1024:.1f} KB read...")
        
        file_wrapper.close()
        print(f"   [OK] Large file read completed: {total_read/1024:.1f} KB total")
    except Exception as e:
        print(f"   [ERROR] Error reading large file: {e}")

def demonstrate_error_scenarios():
    """Demo various error scenarios and recovery"""
    print("\n=== Error Handling Demo ===")
    
    # Try to read non-existent file
    print("1. Attempting to read non-existent file...")
    try:
        file_wrapper = FileAccessWrapper("nonexistent.txt", "r")
        content = file_wrapper.read()
        print("   [WARNING] Unexpected success")
    except Exception as e:
        print(f"   [OK] Expected error caught: {e}")
    
    # Try to write to read-only file
    print("2. Attempting invalid operations...")
    try:
        # Open file in read mode
        file_wrapper = FileAccessWrapper("demo_text.txt", "r")
        # Try to write (should fail)
        file_wrapper.write("This should fail")
        print("   [WARNING] Unexpected success writing to read-only file")
    except Exception as e:
        print(f"   [OK] Expected error caught: {e}")
        try:
            file_wrapper.close()
        except:
            pass
    
    # Test file handle cleanup
    print("3. Testing proper file handle cleanup...")
    try:
        # Use context manager style (if implemented)
        with FileAccessWrapper("demo_text.txt", "r") as f:
            content = f.read(50)
            print(f"   [OK] Read with context manager: {len(content)} chars")
    except Exception as e:
        print(f"   Note: Context manager not implemented: {e}")
        # Fallback to manual cleanup
        try:
            file_wrapper = FileAccessWrapper("demo_text.txt", "r")
            content = file_wrapper.read(50)
            file_wrapper.close()
            print(f"   [OK] Manual cleanup successful: {len(content)} chars")
        except Exception as e2:
            print(f"   [ERROR] Manual cleanup failed: {e2}")

def cleanup_demo_files():
    """Clean up demo files"""
    print("\n=== Cleanup ===")
    demo_files = [
        "demo_text.txt",
        "demo_binary.bin", 
        "demo_append.txt",
        "demo_large.txt"
    ]
    
    for filename in demo_files:
        try:
            # In a real implementation, you would use directory operations
            # For now, just note what would be cleaned up
            print(f"   Would delete: {filename}")
        except Exception as e:
            print(f"   Could not delete {filename}: {e}")

def main():
    """Run comprehensive file operations demo"""
    print("PyFatFs Comprehensive File Operations Demo")
    print("=" * 50)
    
    try:
        # Initialize file system (in real usage, you'd mount a real filesystem)
        print("Initializing file system...")
        result = fatfs.mount("", 0, 1)
        if result == 0:
            print("[OK] File system mounted successfully")
        else:
            print(f"[WARNING] Mount returned code: {result} (continuing with demo)")
        
        # Run all demonstrations
        demonstrate_file_creation()
        demonstrate_file_reading()
        demonstrate_file_positioning()
        demonstrate_append_operations()
        demonstrate_large_file_operations()
        demonstrate_error_scenarios()
        cleanup_demo_files()
        
        print("\n" + "=" * 50)
        print("Demo completed! Check the examples above to understand")
        print("how to use PyFatFs for various file operations.")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
