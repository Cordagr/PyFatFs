/*-----------------------------------------------------------------------*/
/* Working disk I/O module for FatFs Python bindings with memory/file backend */
/*-----------------------------------------------------------------------*/

#include "ff.h"
#include "diskio.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Configuration */
#define SECTOR_SIZE     512
#define TOTAL_SECTORS   8192    /* 4MB virtual disk (8192 * 512 bytes) */
#define DISK_IMAGE_FILE "fatfs_disk.img"

/* Virtual disk storage */
static BYTE* virtual_disk = NULL;
static int disk_initialized = 0;

/* File-based backing store option */
static FILE* disk_file = NULL;
static int use_file_backend = 1;  /* Set to 0 for pure memory backend */

/*-----------------------------------------------------------------------*/
/* Initialize virtual disk storage                                       */
/*-----------------------------------------------------------------------*/
static int init_virtual_disk(void)
{
    if (use_file_backend) {
        /* Try to open existing disk image */
        disk_file = fopen(DISK_IMAGE_FILE, "r+b");
        if (!disk_file) {
            /* Create new disk image */
            disk_file = fopen(DISK_IMAGE_FILE, "w+b");
            if (!disk_file) {
                return 0; /* Failed to create */
            }
            
            /* Initialize with zeros */
            BYTE zero_sector[SECTOR_SIZE];
            memset(zero_sector, 0, SECTOR_SIZE);
            
            for (int i = 0; i < TOTAL_SECTORS; i++) {
                if (fwrite(zero_sector, 1, SECTOR_SIZE, disk_file) != SECTOR_SIZE) {
                    fclose(disk_file);
                    disk_file = NULL;
                    return 0;
                }
            }
            fflush(disk_file);
        }
    } else {
        /* Memory-based backend */
        if (!virtual_disk) {
            virtual_disk = (BYTE*)calloc(TOTAL_SECTORS * SECTOR_SIZE, 1);
            if (!virtual_disk) {
                return 0; /* Memory allocation failed */
            }
        }
    }
    
    disk_initialized = 1;
    return 1;
}

/*-----------------------------------------------------------------------*/
/* Cleanup disk storage                                                  */
/*-----------------------------------------------------------------------*/
static void cleanup_virtual_disk(void)
{
    if (disk_file) {
        fclose(disk_file);
        disk_file = NULL;
    }
    
    if (virtual_disk) {
        free(virtual_disk);
        virtual_disk = NULL;
    }
    
    disk_initialized = 0;
}

/*-----------------------------------------------------------------------*/
/* Get Drive Status                                                      */
/*-----------------------------------------------------------------------*/
DSTATUS disk_status (
    BYTE pdrv        /* Physical drive number to identify the drive */
)
{
    switch (pdrv) {
    case 0:
        return disk_initialized ? 0 : STA_NOINIT;
    default:
        return STA_NOINIT;
    }
}

/*-----------------------------------------------------------------------*/
/* Initialize a Drive                                                    */
/*-----------------------------------------------------------------------*/
DSTATUS disk_initialize (
    BYTE pdrv                /* Physical drive number to identify the drive */
)
{
    switch (pdrv) {
    case 0:
        if (init_virtual_disk()) {
            return 0; /* Success */
        } else {
            return STA_NOINIT; /* Failed to initialize */
        }
    default:
        return STA_NOINIT;
    }
}

/*-----------------------------------------------------------------------*/
/* Read Sector(s)                                                       */
/*-----------------------------------------------------------------------*/
DRESULT disk_read (
    BYTE pdrv,        /* Physical drive number to identify the drive */
    BYTE *buff,        /* Data buffer to store read data */
    LBA_t sector,    /* Start sector in LBA */
    UINT count        /* Number of sectors to read */
)
{
    if (pdrv != 0 || !disk_initialized) {
        return RES_PARERR;
    }
    
    if (sector >= TOTAL_SECTORS || (sector + count) > TOTAL_SECTORS) {
        return RES_PARERR;
    }
    
    if (use_file_backend && disk_file) {
        /* File-based backend */
        if (fseek(disk_file, sector * SECTOR_SIZE, SEEK_SET) != 0) {
            return RES_ERROR;
        }
        
        size_t bytes_to_read = count * SECTOR_SIZE;
        size_t bytes_read = fread(buff, 1, bytes_to_read, disk_file);
        
        if (bytes_read != bytes_to_read) {
            return RES_ERROR;
        }
    } else if (virtual_disk) {
        /* Memory-based backend */
        size_t offset = sector * SECTOR_SIZE;
        size_t bytes_to_copy = count * SECTOR_SIZE;
        memcpy(buff, virtual_disk + offset, bytes_to_copy);
    } else {
        return RES_ERROR;
    }
    
    return RES_OK;
}

/*-----------------------------------------------------------------------*/
/* Write Sector(s)                                                      */
/*-----------------------------------------------------------------------*/
#if FF_FS_READONLY == 0
DRESULT disk_write (
    BYTE pdrv,            /* Physical drive number to identify the drive */
    const BYTE *buff,    /* Data to be written */
    LBA_t sector,        /* Start sector in LBA */
    UINT count            /* Number of sectors to write */
)
{
    if (pdrv != 0 || !disk_initialized) {
        return RES_PARERR;
    }
    
    if (sector >= TOTAL_SECTORS || (sector + count) > TOTAL_SECTORS) {
        return RES_PARERR;
    }
    
    if (use_file_backend && disk_file) {
        /* File-based backend */
        if (fseek(disk_file, sector * SECTOR_SIZE, SEEK_SET) != 0) {
            return RES_ERROR;
        }
        
        size_t bytes_to_write = count * SECTOR_SIZE;
        size_t bytes_written = fwrite(buff, 1, bytes_to_write, disk_file);
        
        if (bytes_written != bytes_to_write) {
            return RES_ERROR;
        }
        
        fflush(disk_file); /* Ensure data is written */
    } else if (virtual_disk) {
        /* Memory-based backend */
        size_t offset = sector * SECTOR_SIZE;
        size_t bytes_to_copy = count * SECTOR_SIZE;
        memcpy(virtual_disk + offset, buff, bytes_to_copy);
    } else {
        return RES_ERROR;
    }
    
    return RES_OK;
}
#endif

/*-----------------------------------------------------------------------*/
/* Miscellaneous Functions                                               */
/*-----------------------------------------------------------------------*/
DRESULT disk_ioctl (
    BYTE pdrv,        /* Physical drive number (0..) */
    BYTE cmd,        /* Control code */
    void *buff        /* Buffer to send/receive control data */
)
{
    if (pdrv != 0) {
        return RES_PARERR;
    }
    
    switch (cmd) {
    case CTRL_SYNC:
        /* Complete pending write process */
        if (use_file_backend && disk_file) {
            fflush(disk_file);
        }
        return RES_OK;
        
    case GET_SECTOR_COUNT:
        *(LBA_t*)buff = TOTAL_SECTORS;
        return RES_OK;
        
    case GET_SECTOR_SIZE:
        *(WORD*)buff = SECTOR_SIZE;
        return RES_OK;
        
    case GET_BLOCK_SIZE:
        *(DWORD*)buff = 1; /* Erase block size in sectors */
        return RES_OK;
        
    default:
        return RES_PARERR;
    }
}

/*-----------------------------------------------------------------------*/
/* Get current time for FatFs timestamps                                */
/*-----------------------------------------------------------------------*/
DWORD get_fattime (void)
{
    /* Return current time in FAT format */
    /* For simplicity, return a fixed timestamp */
    /* Format: bit31:25=Year(0..127 from 1980), bit24:21=Month(1..12), bit20:16=Day(1..31) */
    /*         bit15:11=Hour(0..23), bit10:5=Minute(0..59), bit4:0=Second/2(0..29) */
    
    /* Example: 2025-10-11 14:30:00 */
    /* Year: 2025-1980=45, Month: 10, Day: 11, Hour: 14, Minute: 30, Second: 0 */
    return ((DWORD)(45 << 25)) | ((DWORD)(10 << 21)) | ((DWORD)(11 << 16)) | 
           ((DWORD)(14 << 11)) | ((DWORD)(30 << 5)) | ((DWORD)(0 >> 1));
}

/*-----------------------------------------------------------------------*/
/* Additional helper functions for Python integration                    */
/*-----------------------------------------------------------------------*/

/* Function to format the virtual disk with FAT filesystem */
int format_virtual_disk(void)
{
    if (!disk_initialized) {
        if (!init_virtual_disk()) {
            return 0;
        }
    }
    
    /* This would typically call f_mkfs, but that requires integration with FatFs */
    /* For now, we'll rely on FatFs to handle the formatting when mounting */
    return 1;
}

/* Function to get disk info */
void get_disk_info(DWORD* total_sectors, DWORD* sector_size)
{
    if (total_sectors) *total_sectors = TOTAL_SECTORS;
    if (sector_size) *sector_size = SECTOR_SIZE;
}

/* Cleanup function to be called when Python module unloads */
void cleanup_disk_resources(void)
{
    cleanup_virtual_disk();
}