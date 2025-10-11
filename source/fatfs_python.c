#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "ff.h"
#include "diskio.h"

// External functions from diskio_working.c
extern int format_virtual_disk(void);
extern void get_disk_info(DWORD* total_sectors, DWORD* sector_size);
extern void cleanup_disk_resources(void);

// Global filesystem object
static FATFS* g_fs = NULL;

// Python wrapper functions for FatFs

static PyObject* fatfs_mount(PyObject* self, PyObject* args) {
    const char* path;
    int drive;
    int opt;
    
    if (!PyArg_ParseTuple(args, "sii", &path, &drive, &opt)) {
        return NULL;
    }
    
    if (g_fs) {
        PyMem_Free(g_fs);
        g_fs = NULL;
    }
    
    g_fs = (FATFS*)PyMem_Malloc(sizeof(FATFS));
    if (!g_fs) {
        return PyErr_NoMemory();
    }
    
    FRESULT res = f_mount(g_fs, path, opt);
    
    // If mount fails with "no filesystem", try to format the disk
    if (res == FR_NO_FILESYSTEM) {
        // Try to format the disk using simple format
        BYTE work[512]; // Work area for f_mkfs
        MKFS_PARM parm = {0};
        parm.fmt = FM_ANY;
        res = f_mkfs(path, &parm, work, sizeof(work));
        
        if (res == FR_OK) {
            // Try mounting again after format
            res = f_mount(g_fs, path, opt);
        }
    }
    
    if (res != FR_OK && g_fs) {
        PyMem_Free(g_fs);
        g_fs = NULL;
    }
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_open(PyObject* self, PyObject* args) {
    const char* path;
    int mode;
    
    if (!PyArg_ParseTuple(args, "si", &path, &mode)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)PyMem_Malloc(sizeof(FIL));
    if (!fp) {
        return PyErr_NoMemory();
    }
    
    FRESULT res = f_open(fp, path, mode);
    
    if (res != FR_OK) {
        PyMem_Free(fp);
        // Return error code as integer for failed open
        return PyLong_FromLong((long)res);
    }
    
    // Return file pointer as integer for successful open
    return PyLong_FromVoidPtr(fp);
}

static PyObject* fatfs_close(PyObject* self, PyObject* args) {
    void* fp_ptr;
    
    if (!PyArg_ParseTuple(args, "k", &fp_ptr)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)fp_ptr;
    FRESULT res = f_close(fp);
    PyMem_Free(fp);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_read(PyObject* self, PyObject* args) {
    void* fp_ptr;
    int size;
    
    if (!PyArg_ParseTuple(args, "ki", &fp_ptr, &size)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)fp_ptr;
    char* buffer = (char*)PyMem_Malloc(size);
    if (!buffer) {
        return PyErr_NoMemory();
    }
    
    UINT bytes_read;
    FRESULT res = f_read(fp, buffer, size, &bytes_read);
    
    if (res != FR_OK) {
        PyMem_Free(buffer);
        return PyLong_FromLong(res);
    }
    
    PyObject* result = PyBytes_FromStringAndSize(buffer, bytes_read);
    PyMem_Free(buffer);
    
    return result;
}

static PyObject* fatfs_write(PyObject* self, PyObject* args) {
    void* fp_ptr;
    const char* data;
    Py_ssize_t data_len;
    
    if (!PyArg_ParseTuple(args, "ky#", &fp_ptr, &data, &data_len)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)fp_ptr;
    UINT bytes_written = 0;
    
    FRESULT res = f_write(fp, data, (UINT)data_len, &bytes_written);
    
    return Py_BuildValue("(ii)", res, bytes_written);
}

static PyObject* fatfs_format(PyObject* self, PyObject* args) {
    const char* path;
    
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    
    BYTE work[512]; // Work area for f_mkfs
    MKFS_PARM parm = {0};
    parm.fmt = FM_ANY;
    FRESULT res = f_mkfs(path, &parm, work, sizeof(work));
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_get_disk_info(PyObject* self, PyObject* args) {
    DWORD total_sectors, sector_size;
    get_disk_info(&total_sectors, &sector_size);
    
    return Py_BuildValue("(ii)", total_sectors, sector_size);
}

// Method definitions
static PyMethodDef fatfs_methods[] = {
    {"mount", fatfs_mount, METH_VARARGS, "Mount a filesystem"},
    {"open", fatfs_open, METH_VARARGS, "Open a file"},
    {"close", fatfs_close, METH_VARARGS, "Close a file"},
    {"read", fatfs_read, METH_VARARGS, "Read from a file"},
    {"write", fatfs_write, METH_VARARGS, "Write to a file"},
    {"format", fatfs_format, METH_VARARGS, "Format a filesystem"},
    {"get_disk_info", fatfs_get_disk_info, METH_VARARGS, "Get disk information"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef fatfs_module = {
    PyModuleDef_HEAD_INIT,
    "fatfs",
    "Python bindings for FatFs library with working disk I/O",
    -1,
    fatfs_methods
};

// Module initialization
PyMODINIT_FUNC PyInit_fatfs(void) {
    return PyModule_Create(&fatfs_module);
}