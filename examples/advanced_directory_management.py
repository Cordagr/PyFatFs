#!/usr/bin/env python3
"""
Advanced Directory Management Demo for PyFatFs

This demo showcases sophisticated directory operations including:
- Creating nested directory structures
- Traversing directory trees
- Directory metadata and statistics
- Moving and organizing files
- Directory cleanup and management
- Path operations and validation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyfatfs import DirectoryAccessWrapper, FileAccessWrapper
import fatfs

class DirectoryDemo:
    def __init__(self):
        self.created_dirs = []
        self.created_files = []
    
    def create_sample_structure(self):
        """Create a complex directory structure for demonstration"""
        print("=== Creating Sample Directory Structure ===")
        
        # Define directory structure
        directories = [
            "projects",
            "projects/web_app",
            "projects/web_app/src",
            "projects/web_app/src/components",
            "projects/web_app/src/utils",
            "projects/web_app/tests",
            "projects/mobile_app", 
            "projects/mobile_app/android",
            "projects/mobile_app/ios",
            "documents",
            "documents/reports",
            "documents/presentations",
            "media",
            "media/images",
            "media/videos",
            "media/audio"
        ]
        
        # Create directories
        for dir_path in directories:
            try:
                dir_wrapper = DirectoryAccessWrapper(dir_path)
                dir_wrapper.mkdir()
                self.created_dirs.append(dir_path)
                print(f"   [OK] Created: {dir_path}")
            except Exception as e:
                print(f"   [ERROR] Failed to create {dir_path}: {e}")
        
        # Create sample files in various directories
        sample_files = [
            ("projects/web_app/README.md", "# Web Application\n\nThis is a sample web app project."),
            ("projects/web_app/src/main.js", "// Main application entry point\nconsole.log('Hello World');"),
            ("projects/web_app/src/components/header.js", "// Header component\nfunction Header() { return 'Header'; }"),
            ("projects/web_app/src/utils/helpers.js", "// Utility functions\nfunction formatDate(date) { return date.toString(); }"),
            ("projects/web_app/tests/main.test.js", "// Main tests\ntest('basic test', () => { expect(true).toBe(true); });"),
            ("projects/mobile_app/README.md", "# Mobile Application\n\nCross-platform mobile app."),
            ("documents/reports/quarterly_report.txt", "Q4 2024 Report\n\nSales increased by 15%."),
            ("documents/presentations/project_overview.txt", "Project Overview\n\n1. Introduction\n2. Goals\n3. Timeline"),
            ("media/images/logo.txt", "This would be a logo image file."),
            ("media/videos/demo.txt", "This would be a demo video file."),
        ]
        
        print("\n--- Creating Sample Files ---")
        for file_path, content in sample_files:
            try:
                file_wrapper = FileAccessWrapper(file_path, "w")
                file_wrapper.write(content)
                file_wrapper.close()
                self.created_files.append(file_path)
                print(f"   [OK] Created: {file_path}")
            except Exception as e:
                print(f"   [ERROR] Failed to create {file_path}: {e}")
    
    def demonstrate_directory_listing(self):
        """Demo listing directory contents with details"""
        print("\n=== Directory Listing Demo ===")
        
        # List root level
        print("1. Root directory contents:")
        try:
            root_wrapper = DirectoryAccessWrapper(".")
            entries = root_wrapper.listdir()
            for entry in entries[:10]:  # Limit output
                print(f"   {entry}")
            if len(entries) > 10:
                print(f"   ... and {len(entries) - 10} more entries")
        except Exception as e:
            print(f"   [ERROR] Error listing root: {e}")
        
        # List specific directories
        test_dirs = ["projects", "projects/web_app", "documents"]
        for dir_path in test_dirs:
            print(f"\n2. Contents of '{dir_path}':")
            try:
                dir_wrapper = DirectoryAccessWrapper(dir_path)
                entries = dir_wrapper.listdir()
                if entries:
                    for entry in entries:
                        # Try to determine if it's a file or directory
                        full_path = f"{dir_path}/{entry}" if dir_path != "." else entry
                        try:
                            # Try to open as directory
                            test_dir = DirectoryAccessWrapper(full_path)
                            test_entries = test_dir.listdir()
                            print(f"   📁 {entry}/ ({len(test_entries)} items)")
                        except:
                            # Must be a file
                            print(f"   📄 {entry}")
                else:
                    print("   (empty)")
            except Exception as e:
                print(f"   [ERROR] Error listing {dir_path}: {e}")
    
    def demonstrate_directory_traversal(self):
        """Demo recursive directory traversal"""
        print("\n=== Directory Traversal Demo ===")
        
        def traverse_directory(path, level=0):
            """Recursively traverse directory structure"""
            indent = "  " * level
            try:
                dir_wrapper = DirectoryAccessWrapper(path)
                entries = dir_wrapper.listdir()
                
                for entry in entries:
                    full_path = f"{path}/{entry}" if path != "." else entry
                    try:
                        # Try to list as directory
                        sub_dir = DirectoryAccessWrapper(full_path)
                        sub_entries = sub_dir.listdir()
                        print(f"{indent}📁 {entry}/ ({len(sub_entries)} items)")
                        
                        # Recursively traverse subdirectories (limit depth)
                        if level < 3:
                            traverse_directory(full_path, level + 1)
                    except:
                        # Must be a file
                        print(f"{indent}📄 {entry}")
            except Exception as e:
                print(f"{indent}[ERROR] Error accessing {path}: {e}")
        
        print("1. Complete directory tree:")
        traverse_directory("projects", 0)
    
    def demonstrate_directory_statistics(self):
        """Demo gathering directory statistics"""
        print("\n=== Directory Statistics Demo ===")
        
        def get_directory_stats(path):
            """Get statistics for a directory"""
            stats = {
                'total_dirs': 0,
                'total_files': 0,
                'total_size': 0,
                'max_depth': 0
            }
            
            def count_recursive(dir_path, depth=0):
                try:
                    dir_wrapper = DirectoryAccessWrapper(dir_path)
                    entries = dir_wrapper.listdir()
                    stats['max_depth'] = max(stats['max_depth'], depth)
                    
                    for entry in entries:
                        full_path = f"{dir_path}/{entry}" if dir_path != "." else entry
                        try:
                            # Try as directory
                            sub_dir = DirectoryAccessWrapper(full_path)
                            sub_dir.listdir()  # Test if it's really a directory
                            stats['total_dirs'] += 1
                            count_recursive(full_path, depth + 1)
                        except:
                            # Must be a file
                            stats['total_files'] += 1
                            try:
                                # Try to get file size
                                file_wrapper = FileAccessWrapper(full_path, "r")
                                content = file_wrapper.read()
                                stats['total_size'] += len(content)
                                file_wrapper.close()
                            except:
                                pass  # Can't read file
                except Exception:
                    pass  # Can't access directory
            
            count_recursive(path)
            return stats
        
        # Get statistics for different directories
        test_paths = ["projects", "documents", "media"]
        for path in test_paths:
            print(f"\n1. Statistics for '{path}':")
            stats = get_directory_stats(path)
            print(f"   Directories: {stats['total_dirs']}")
            print(f"   Files: {stats['total_files']}")
            print(f"   Total size: {stats['total_size']} bytes")
            print(f"   Max depth: {stats['max_depth']}")
    
    def demonstrate_directory_operations(self):
        """Demo advanced directory operations"""
        print("\n=== Advanced Directory Operations Demo ===")
        
        # Create a test directory for operations
        print("1. Creating test workspace...")
        try:
            test_dir = DirectoryAccessWrapper("test_workspace")
            test_dir.mkdir()
            print("   [OK] Test workspace created")
            
            # Create subdirectories
            for subdir in ["temp", "backup", "archive"]:
                sub_wrapper = DirectoryAccessWrapper(f"test_workspace/{subdir}")
                sub_wrapper.mkdir()
                print(f"   [OK] Created subdirectory: {subdir}")
                
        except Exception as e:
            print(f"   [ERROR] Error creating test workspace: {e}")
        
        # Create test files
        print("\n2. Creating test files...")
        test_files = [
            ("test_workspace/file1.txt", "Content of file 1"),
            ("test_workspace/file2.txt", "Content of file 2"),
            ("test_workspace/temp/temp_file.txt", "Temporary content"),
        ]
        
        for file_path, content in test_files:
            try:
                file_wrapper = FileAccessWrapper(file_path, "w")
                file_wrapper.write(content)
                file_wrapper.close()
                print(f"   [OK] Created: {file_path}")
            except Exception as e:
                print(f"   [ERROR] Failed to create {file_path}: {e}")
        
        # Demonstrate copying/moving simulation
        print("\n3. Simulating file organization operations...")
        print("   Note: Actual move/copy operations would require additional implementation")
        print("   - Move temp files to archive")
        print("   - Backup important files")
        print("   - Organize files by type")
    
    def demonstrate_path_operations(self):
        """Demo path manipulation and validation"""
        print("\n=== Path Operations Demo ===")
        
        test_paths = [
            "projects/web_app/src/main.js",
            "documents/../projects/web_app",
            "media/images/./logo.txt",
            "/absolute/path/test",
            "projects//double//slash",
            ""
        ]
        
        print("1. Path validation and normalization:")
        for path in test_paths:
            print(f"   Input: '{path}'")
            
            # Basic path validation
            if not path:
                print("     [ERROR] Empty path")
                continue
            
            # Check for invalid characters (basic check)
            invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
            has_invalid = any(char in path for char in invalid_chars)
            if has_invalid:
                print("     [ERROR] Contains invalid characters")
                continue
            
            # Normalize path (basic implementation)
            normalized = path.replace('//', '/').replace('/./', '/')
            if normalized != path:
                print(f"     → Normalized: '{normalized}'")
            else:
                print("     [OK] Path is valid")
    
    def cleanup_demo_structure(self):
        """Clean up the demo directory structure"""
        print("\n=== Cleanup Demo Structure ===")
        
        # In a real implementation, you would recursively delete directories
        # For now, just show what would be cleaned up
        print("Files that would be deleted:")
        for file_path in reversed(self.created_files):
            print(f"   - {file_path}")
        
        print("\nDirectories that would be deleted:")
        for dir_path in reversed(self.created_dirs):
            print(f"   - {dir_path}/")
        
        print("   Note: Actual deletion requires proper directory removal implementation")

def main():
    """Run comprehensive directory management demo"""
    print("PyFatFs Advanced Directory Management Demo")
    print("=" * 55)
    
    try:
        # Initialize file system
        print("Initializing file system...")
        result = fatfs.mount("", 0, 1)
        if result == 0:
            print("[OK] File system mounted successfully")
        else:
            print(f"[WARNING] Mount returned code: {result} (continuing with demo)")
        
        # Create demo instance and run demonstrations
        demo = DirectoryDemo()
        
        demo.create_sample_structure()
        demo.demonstrate_directory_listing()
        demo.demonstrate_directory_traversal()
        demo.demonstrate_directory_statistics()
        demo.demonstrate_directory_operations()
        demo.demonstrate_path_operations()
        demo.cleanup_demo_structure()
        
        print("\n" + "=" * 55)
        print("Directory management demo completed!")
        print("This demo showed advanced directory operations including:")
        print("- Complex directory structure creation")
        print("- Recursive directory traversal")
        print("- Directory statistics gathering")
        print("- Path validation and normalization")
        print("- File organization concepts")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
