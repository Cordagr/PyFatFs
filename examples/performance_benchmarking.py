#!/usr/bin/env python3
"""
Performance Benchmarking and Optimization Demo for PyFatFs

This demo focuses on:
- Performance measurement and benchmarking
- Memory usage optimization
- Large file handling strategies
- Concurrent access patterns
- Buffer size optimization
- Cache effectiveness analysis
"""

import sys
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyfatfs import FileAccessWrapper, DirectoryAccessWrapper
import fatfs

class PerformanceBenchmark:
    def __init__(self):
        self.results = {}
        self.test_data_sizes = [1024, 8192, 65536, 262144, 1048576]  # 1KB to 1MB
    
    def time_operation(self, operation_name, operation_func):
        """Time an operation and store results"""
        print(f"   Running {operation_name}...")
        start_time = time.time()
        
        try:
            result = operation_func()
            end_time = time.time()
            duration = end_time - start_time
            
            self.results[operation_name] = {
                'duration': duration,
                'success': True,
                'result': result
            }
            print(f"   [OK] {operation_name}: {duration:.4f} seconds")
            return result
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            self.results[operation_name] = {
                'duration': duration,
                'success': False,
                'error': str(e)
            }
            print(f"   [ERROR] {operation_name} failed: {e}")
            return None
    
    def benchmark_file_creation(self):
        """Benchmark file creation with different sizes"""
        print("\n=== File Creation Performance ===")
        
        for size in self.test_data_sizes:
            size_name = self.format_size(size)
            test_data = "A" * size
            
            def create_file():
                filename = f"perf_test_{size}.txt"
                file_wrapper = FileAccessWrapper(filename, "w")
                file_wrapper.write(test_data)
                file_wrapper.close()
                return size
            
            self.time_operation(f"Create {size_name} file", create_file)
    
    def benchmark_file_reading(self):
        """Benchmark file reading with different buffer sizes"""
        print("\n=== File Reading Performance ===")
        
        # First create a test file
        test_size = 1048576  # 1MB
        test_data = "B" * test_size
        test_filename = "read_perf_test.txt"
        
        print("   Creating test file for reading benchmark...")
        try:
            file_wrapper = FileAccessWrapper(test_filename, "w")
            file_wrapper.write(test_data)
            file_wrapper.close()
        except Exception as e:
            print(f"   [ERROR] Failed to create test file: {e}")
            return
        
        # Test different buffer sizes
        buffer_sizes = [512, 1024, 4096, 8192, 16384, 65536]
        
        for buffer_size in buffer_sizes:
            def read_with_buffer():
                file_wrapper = FileAccessWrapper(test_filename, "r")
                total_read = 0
                while True:
                    chunk = file_wrapper.read(buffer_size)
                    if not chunk:
                        break
                    total_read += len(chunk)
                file_wrapper.close()
                return total_read
            
            buffer_name = self.format_size(buffer_size)
            self.time_operation(f"Read 1MB with {buffer_name} buffer", read_with_buffer)
    
    def benchmark_sequential_vs_random_access(self):
        """Compare sequential vs random access patterns"""
        print("\n=== Sequential vs Random Access ===")
        
        # Create test file with known content
        test_filename = "access_pattern_test.txt"
        lines_count = 1000
        line_length = 100
        
        print("   Creating structured test file...")
        try:
            file_wrapper = FileAccessWrapper(test_filename, "w")
            for i in range(lines_count):
                line = f"Line {i:04d}: " + "X" * (line_length - 15) + "\n"
                file_wrapper.write(line)
            file_wrapper.close()
        except Exception as e:
            print(f"   [ERROR] Failed to create test file: {e}")
            return
        
        # Sequential access test
        def sequential_access():
            file_wrapper = FileAccessWrapper(test_filename, "r")
            lines_read = 0
            while True:
                line = file_wrapper.read(line_length)
                if not line:
                    break
                lines_read += 1
            file_wrapper.close()
            return lines_read
        
        self.time_operation("Sequential access", sequential_access)
        
        # Random access test (simulated)
        def random_access():
            file_wrapper = FileAccessWrapper(test_filename, "r")
            reads_performed = 0
            
            # Simulate random access by seeking to different positions
            positions = [i * line_length for i in range(0, lines_count, 10)]
            for pos in positions:
                try:
                    file_wrapper.seek(pos)
                    data = file_wrapper.read(line_length)
                    reads_performed += 1
                except:
                    break
            
            file_wrapper.close()
            return reads_performed
        
        self.time_operation("Random access (every 10th line)", random_access)
    
    def benchmark_concurrent_access(self):
        """Benchmark concurrent file access"""
        print("\n=== Concurrent Access Performance ===")
        
        # Create multiple test files
        num_files = 5
        file_content = "Concurrent test data " * 100
        
        print("   Creating test files for concurrent access...")
        for i in range(num_files):
            try:
                filename = f"concurrent_test_{i}.txt"
                file_wrapper = FileAccessWrapper(filename, "w")
                file_wrapper.write(file_content)
                file_wrapper.close()
            except Exception as e:
                print(f"   [ERROR] Failed to create test file {i}: {e}")
        
        # Sequential access to all files
        def sequential_file_access():
            total_read = 0
            for i in range(num_files):
                try:
                    filename = f"concurrent_test_{i}.txt"
                    file_wrapper = FileAccessWrapper(filename, "r")
                    content = file_wrapper.read()
                    total_read += len(content)
                    file_wrapper.close()
                except Exception as e:
                    print(f"     Error reading file {i}: {e}")
            return total_read
        
        self.time_operation("Sequential access to 5 files", sequential_file_access)
        
        # Simulate concurrent access (Note: real concurrent access would require thread-safe implementation)
        def simulated_concurrent_access():
            """Simulate concurrent access by rapid switching between files"""
            total_read = 0
            open_files = []
            
            # Open all files
            for i in range(num_files):
                try:
                    filename = f"concurrent_test_{i}.txt"
                    file_wrapper = FileAccessWrapper(filename, "r")
                    open_files.append(file_wrapper)
                except Exception as e:
                    print(f"     Error opening file {i}: {e}")
            
            # Read from files in round-robin fashion
            chunk_size = 100
            for _ in range(10):  # 10 rounds
                for file_wrapper in open_files:
                    try:
                        chunk = file_wrapper.read(chunk_size)
                        total_read += len(chunk)
                    except Exception as e:
                        pass
            
            # Close all files
            for file_wrapper in open_files:
                try:
                    file_wrapper.close()
                except:
                    pass
            
            return total_read
        
        self.time_operation("Simulated concurrent access", simulated_concurrent_access)
    
    def benchmark_directory_operations(self):
        """Benchmark directory operations"""
        print("\n=== Directory Operations Performance ===")
        
        # Create many directories
        def create_many_directories():
            base_dir = "perf_test_dirs"
            try:
                base_wrapper = DirectoryAccessWrapper(base_dir)
                base_wrapper.mkdir()
            except:
                pass
            
            dirs_created = 0
            for i in range(100):
                try:
                    dir_path = f"{base_dir}/dir_{i:03d}"
                    dir_wrapper = DirectoryAccessWrapper(dir_path)
                    dir_wrapper.mkdir()
                    dirs_created += 1
                except Exception as e:
                    break
            return dirs_created
        
        self.time_operation("Create 100 directories", create_many_directories)
        
        # List directory with many entries
        def list_large_directory():
            try:
                base_wrapper = DirectoryAccessWrapper("perf_test_dirs")
                entries = base_wrapper.listdir()
                return len(entries)
            except Exception as e:
                return 0
        
        self.time_operation("List directory with 100 entries", list_large_directory)
    
    def benchmark_memory_usage(self):
        """Analyze memory usage patterns"""
        print("\n=== Memory Usage Analysis ===")
        
        # Test memory usage with large file operations
        large_data = "M" * (1024 * 1024)  # 1MB string
        
        def large_file_write():
            try:
                file_wrapper = FileAccessWrapper("memory_test_large.txt", "w")
                file_wrapper.write(large_data)
                file_wrapper.close()
                return len(large_data)
            except Exception as e:
                return 0
        
        self.time_operation("Write 1MB file (memory intensive)", large_file_write)
        
        # Test chunked writing (memory efficient)
        def chunked_file_write():
            chunk_size = 8192
            total_written = 0
            try:
                file_wrapper = FileAccessWrapper("memory_test_chunked.txt", "w")
                for i in range(0, len(large_data), chunk_size):
                    chunk = large_data[i:i + chunk_size]
                    file_wrapper.write(chunk)
                    total_written += len(chunk)
                file_wrapper.close()
                return total_written
            except Exception as e:
                return total_written
        
        self.time_operation("Write 1MB file (chunked, memory efficient)", chunked_file_write)
    
    def format_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes // 1024}KB"
        else:
            return f"{size_bytes // (1024 * 1024)}MB"
    
    def print_performance_summary(self):
        """Print a summary of all performance results"""
        print("\n" + "=" * 60)
        print("PERFORMANCE BENCHMARK SUMMARY")
        print("=" * 60)
        
        if not self.results:
            print("No benchmark results available.")
            return
        
        successful_tests = [name for name, result in self.results.items() if result['success']]
        failed_tests = [name for name, result in self.results.items() if not result['success']]
        
        print(f"Total tests run: {len(self.results)}")
        print(f"Successful: {len(successful_tests)}")
        print(f"Failed: {len(failed_tests)}")
        
        if successful_tests:
            print("\n--- Successful Operations (sorted by duration) ---")
            sorted_results = sorted(
                [(name, self.results[name]) for name in successful_tests],
                key=lambda x: x[1]['duration']
            )
            
            for name, result in sorted_results:
                duration = result['duration']
                print(f"  {duration:8.4f}s - {name}")
        
        if failed_tests:
            print("\n--- Failed Operations ---")
            for name in failed_tests:
                error = self.results[name]['error']
                print(f"  [ERROR] {name}: {error}")
        
        # Performance insights
        print("\n--- Performance Insights ---")
        if successful_tests:
            durations = [self.results[name]['duration'] for name in successful_tests]
            avg_duration = sum(durations) / len(durations)
            print(f"  Average operation time: {avg_duration:.4f}s")
            print(f"  Fastest operation: {min(durations):.4f}s")
            print(f"  Slowest operation: {max(durations):.4f}s")
        
        print("\n--- Recommendations ---")
        print("  • Use appropriate buffer sizes for your use case")
        print("  • Consider chunked operations for large files")
        print("  • Sequential access is typically faster than random access")
        print("  • Monitor memory usage with large file operations")
        print("  • Test your specific use case for optimal performance")

def main():
    """Run comprehensive performance benchmark"""
    print("PyFatFs Performance Benchmarking and Optimization Demo")
    print("=" * 65)
    
    try:
        # Initialize file system
        print("Initializing file system...")
        result = fatfs.mount("", 0, 1)
        if result == 0:
            print("[OK] File system mounted successfully")
        else:
            print(f"[WARNING] Mount returned code: {result} (continuing with demo)")
        
        # Create benchmark instance and run tests
        benchmark = PerformanceBenchmark()
        
        print("\nStarting performance benchmarks...")
        print("This may take a few moments to complete.\n")
        
        benchmark.benchmark_file_creation()
        benchmark.benchmark_file_reading()
        benchmark.benchmark_sequential_vs_random_access()
        benchmark.benchmark_concurrent_access()
        benchmark.benchmark_directory_operations()
        benchmark.benchmark_memory_usage()
        
        benchmark.print_performance_summary()
        
        print("\n" + "=" * 65)
        print("Performance benchmarking completed!")
        print("Use these results to optimize your PyFatFs usage patterns.")
        
    except Exception as e:
        print(f"Benchmark failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()