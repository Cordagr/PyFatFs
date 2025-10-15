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
    
    // Return file pointer as unsigned long long for successful open
    return PyLong_FromUnsignedLongLong((unsigned long long)(uintptr_t)fp);
}

static PyObject* fatfs_close(PyObject* self, PyObject* args) {
    unsigned long long fp_ptr;
    
    if (!PyArg_ParseTuple(args, "K", &fp_ptr)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
    FRESULT res = f_close(fp);
    PyMem_Free(fp);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_read(PyObject* self, PyObject* args) {
    unsigned long long fp_ptr;
    int size;
    
    if (!PyArg_ParseTuple(args, "Ki", &fp_ptr, &size)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
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
    unsigned long long fp_ptr;
    const char* data;
    Py_ssize_t data_len;
    
    if (!PyArg_ParseTuple(args, "Ky#", &fp_ptr, &data, &data_len)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
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

// Extended file operations
static PyObject* fatfs_lseek(PyObject* self, PyObject* args) {
    unsigned long long fp_ptr;
    unsigned long offset;
    
    if (!PyArg_ParseTuple(args, "Kk", &fp_ptr, &offset)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
    FRESULT res = f_lseek(fp, offset);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_truncate(PyObject* self, PyObject* args) {
    unsigned long long fp_ptr;
    
    if (!PyArg_ParseTuple(args, "K", &fp_ptr)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
    FRESULT res = f_truncate(fp);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_sync(PyObject* self, PyObject* args) {
    unsigned long long fp_ptr;
    
    if (!PyArg_ParseTuple(args, "K", &fp_ptr)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
    FRESULT res = f_sync(fp);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_tell(PyObject* self, PyObject* args) {
    unsigned long long fp_ptr;
    
    if (!PyArg_ParseTuple(args, "K", &fp_ptr)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
    FSIZE_t pos = f_tell(fp);
    
    return PyLong_FromUnsignedLongLong(pos);
}

static PyObject* fatfs_eof(PyObject* self, PyObject* args) {
    unsigned long long fp_ptr;
    
    if (!PyArg_ParseTuple(args, "K", &fp_ptr)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
    int eof = f_eof(fp);
    
    return PyBool_FromLong(eof);
}

static PyObject* fatfs_size(PyObject* self, PyObject* args) {
    unsigned long long fp_ptr;
    
    if (!PyArg_ParseTuple(args, "K", &fp_ptr)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
    FSIZE_t size = f_size(fp);
    
    return PyLong_FromUnsignedLongLong(size);
}

static PyObject* fatfs_error(PyObject* self, PyObject* args) {
    unsigned long long fp_ptr;
    
    if (!PyArg_ParseTuple(args, "K", &fp_ptr)) {
        return NULL;
    }
    
    FIL* fp = (FIL*)(uintptr_t)fp_ptr;
    int error = f_error(fp);
    
    return PyBool_FromLong(error);
}

// Directory operations
static PyObject* fatfs_opendir(PyObject* self, PyObject* args) {
    const char* path;
    
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    
    DIR* dp = (DIR*)PyMem_Malloc(sizeof(DIR));
    if (!dp) {
        return PyErr_NoMemory();
    }
    
    FRESULT res = f_opendir(dp, path);
    
    if (res != FR_OK) {
        PyMem_Free(dp);
        return PyLong_FromLong((long)res);
    }
    
    return PyLong_FromUnsignedLongLong((unsigned long long)(uintptr_t)dp);
}

static PyObject* fatfs_closedir(PyObject* self, PyObject* args) {
    unsigned long long dp_ptr;
    
    if (!PyArg_ParseTuple(args, "K", &dp_ptr)) {
        return NULL;
    }
    
    DIR* dp = (DIR*)(uintptr_t)dp_ptr;
    FRESULT res = f_closedir(dp);
    PyMem_Free(dp);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_readdir(PyObject* self, PyObject* args) {
    unsigned long long dp_ptr;
    
    if (!PyArg_ParseTuple(args, "K", &dp_ptr)) {
        return NULL;
    }
    
    DIR* dp = (DIR*)(uintptr_t)dp_ptr;
    FILINFO fno;
    FRESULT res = f_readdir(dp, &fno);
    
    if (res != FR_OK) {
        return PyLong_FromLong(res);
    }
    
    if (fno.fname[0] == 0) {
        // End of directory
        Py_RETURN_NONE;
    }
    
    return Py_BuildValue("{s:s,s:K,s:i,s:i,s:i,s:i,s:i,s:i}",
        "fname", fno.fname,
        "fsize", (unsigned long long)fno.fsize,
        "fdate", fno.fdate,
        "ftime", fno.ftime,
        "fattrib", fno.fattrib,
        "year", (fno.fdate >> 9) + 1980,
        "month", (fno.fdate >> 5) & 15,
        "day", fno.fdate & 31);
}

// File and directory management
static PyObject* fatfs_stat(PyObject* self, PyObject* args) {
    const char* path;
    
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    
    FILINFO fno;
    FRESULT res = f_stat(path, &fno);
    
    if (res != FR_OK) {
        return PyLong_FromLong(res);
    }
    
    return Py_BuildValue("{s:s,s:K,s:i,s:i,s:i,s:i,s:i,s:i}",
        "fname", fno.fname,
        "fsize", (unsigned long long)fno.fsize,
        "fdate", fno.fdate,
        "ftime", fno.ftime,
        "fattrib", fno.fattrib,
        "year", (fno.fdate >> 9) + 1980,
        "month", (fno.fdate >> 5) & 15,
        "day", fno.fdate & 31);
}

static PyObject* fatfs_unlink(PyObject* self, PyObject* args) {
    const char* path;
    
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    
    FRESULT res = f_unlink(path);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_rename(PyObject* self, PyObject* args) {
    const char* old_name;
    const char* new_name;
    
    if (!PyArg_ParseTuple(args, "ss", &old_name, &new_name)) {
        return NULL;
    }
    
    FRESULT res = f_rename(old_name, new_name);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_chmod(PyObject* self, PyObject* args) {
    const char* path;
    int attr;
    int mask;
    
    if (!PyArg_ParseTuple(args, "sii", &path, &attr, &mask)) {
        return NULL;
    }
    
    FRESULT res = f_chmod(path, attr, mask);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_mkdir(PyObject* self, PyObject* args) {
    const char* path;
    
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    
    FRESULT res = f_mkdir(path);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_chdir(PyObject* self, PyObject* args) {
    const char* path;
    
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    
    FRESULT res = f_chdir(path);
    
    return PyLong_FromLong(res);
}

static PyObject* fatfs_getcwd(PyObject* self, PyObject* args) {
    char buff[256];
    FRESULT res = f_getcwd(buff, sizeof(buff));
    
    if (res != FR_OK) {
        return PyLong_FromLong(res);
    }
    
    return PyUnicode_FromString(buff);
}

// Volume management
static PyObject* fatfs_getfree(PyObject* self, PyObject* args) {
    const char* path;
    
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    
    DWORD fre_clust;
    FATFS* fs;
    FRESULT res = f_getfree(path, &fre_clust, &fs);
    
    if (res != FR_OK) {
        return PyLong_FromLong(res);
    }
    
    DWORD fre_sect = fre_clust * fs->csize;
    DWORD tot_sect = (fs->n_fatent - 2) * fs->csize;
    
    return Py_BuildValue("{s:k,s:k,s:k,s:k}",
        "free_clusters", fre_clust,
        "total_clusters", fs->n_fatent - 2,
        "free_sectors", fre_sect,
        "total_sectors", tot_sect);
}

static PyObject* fatfs_getlabel(PyObject* self, PyObject* args) {
    const char* path;
    
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    
    char label[12];
    DWORD vsn;
    FRESULT res = f_getlabel(path, label, &vsn);
    
    if (res != FR_OK) {
        return PyLong_FromLong(res);
    }
    
    return Py_BuildValue("{s:s,s:k}", "label", label, "serial", vsn);
}

static PyObject* fatfs_setlabel(PyObject* self, PyObject* args) {
    const char* label;
    
    if (!PyArg_ParseTuple(args, "s", &label)) {
        return NULL;
    }
    
    FRESULT res = f_setlabel(label);
    
    return PyLong_FromLong(res);
}

// Method definitions
static PyMethodDef fatfs_methods[] = {
    // Core functions
    {"mount", fatfs_mount, METH_VARARGS, "Mount a filesystem"},
    {"open", fatfs_open, METH_VARARGS, "Open a file"},
    {"close", fatfs_close, METH_VARARGS, "Close a file"},
    {"read", fatfs_read, METH_VARARGS, "Read from a file"},
    {"write", fatfs_write, METH_VARARGS, "Write to a file"},
    {"format", fatfs_format, METH_VARARGS, "Format a filesystem"},
    {"get_disk_info", fatfs_get_disk_info, METH_VARARGS, "Get disk information"},
    
    // Extended file operations
    {"lseek", fatfs_lseek, METH_VARARGS, "Move read/write pointer"},
    {"truncate", fatfs_truncate, METH_VARARGS, "Truncate file size"},
    {"sync", fatfs_sync, METH_VARARGS, "Flush cached data"},
    {"tell", fatfs_tell, METH_VARARGS, "Get current read/write pointer"},
    {"eof", fatfs_eof, METH_VARARGS, "Test for end-of-file"},
    {"size", fatfs_size, METH_VARARGS, "Get file size"},
    {"error", fatfs_error, METH_VARARGS, "Test for file error"},
    
    // Directory operations
    {"opendir", fatfs_opendir, METH_VARARGS, "Open a directory"},
    {"closedir", fatfs_closedir, METH_VARARGS, "Close a directory"},
    {"readdir", fatfs_readdir, METH_VARARGS, "Read directory entry"},
    
    // File and directory management
    {"stat", fatfs_stat, METH_VARARGS, "Get file/directory status"},
    {"unlink", fatfs_unlink, METH_VARARGS, "Remove a file or directory"},
    {"rename", fatfs_rename, METH_VARARGS, "Rename/move a file or directory"},
    {"chmod", fatfs_chmod, METH_VARARGS, "Change file attributes"},
    {"mkdir", fatfs_mkdir, METH_VARARGS, "Create a directory"},
    {"chdir", fatfs_chdir, METH_VARARGS, "Change current directory"},
    {"getcwd", fatfs_getcwd, METH_VARARGS, "Get current working directory"},
    
    // Volume management
    {"getfree", fatfs_getfree, METH_VARARGS, "Get free space information"},
    {"getlabel", fatfs_getlabel, METH_VARARGS, "Get volume label"},
    {"setlabel", fatfs_setlabel, METH_VARARGS, "Set volume label"},
    
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