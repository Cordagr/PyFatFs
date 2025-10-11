## Installation


### Core Functions

- `mount(path, drive, opt)`: Mount filesystem
- `open_file(path, mode)`: Open file
- `get_error_string(code)`: Get error message

### File Operations

- `FatFsFile.read(size)`: Read data
- `FatFsFile.write(data)`: Write data
- `FatFsFile.close()`: Close file

### File Manager

- `FatFsFileManager.mount_filesystem()`: Mount filesystem
- `FatFsFileManager.file_exists()`: Check file existence
- `FatFsFileManager.get_file_size()`: Get file size
- `FatFsFileManager.copy_file()`: Copy file

## Limitations

Current implementation includes:

- Basic file operations (read, write, open, close)
- File mounting
- Error handling

Not yet implemented:

- Directory operations (mkdir, rmdir, listdir)
- File deletion and renaming
- File attributes and timestamps
- Advanced filesystem operations

These features require additional C extension functions and will be added in future versions.

## Development

### Building

```bash
# Clean build
python setup.py clean --all
python setup.py build_ext --inplace

# Install in development mode
pip install -e .
```

### Testing

```bash
# Run examples
python examples/basic_file_ops.py
python examples/file_manager_demo.py
python examples/error_handling.py
```

## Credits

- FatFs library by ChaN

## Support

For issues and questions:

1. Check the examples directory
2. Review the API documentation
3. Open an issue on the repository
4. Check FatFs documentation for low-level details
