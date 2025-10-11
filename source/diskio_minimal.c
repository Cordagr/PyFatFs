/*-----------------------------------------------------------------------*/
/* Minimal Low level disk I/O module for FatFs Python bindings          */
/*-----------------------------------------------------------------------*/

#include "ff.h"			/* Basic definitions of FatFs */
#include "diskio.h"		/* Declarations FatFs MAI */

/* Mapping of physical drive number for each drive */
#define DEV_FLASH	0	/* Map FTL to physical drive 0 */
#define DEV_MMC		1	/* Map MMC/SD card to physical drive 1 */
#define DEV_USB		2	/* Map USB MSD to physical drive 2 */

/*-----------------------------------------------------------------------*/
/* Get Drive Status                                                      */
/*-----------------------------------------------------------------------*/

DSTATUS disk_status (
	BYTE pdrv		/* Physical drive number to identify the drive */
)
{
	DSTATUS stat;

	switch (pdrv) {
	case DEV_FLASH :
		stat = 0; /* Assume ready */
		break;

	case DEV_MMC :
		stat = 0; /* Assume ready */
		break;

	case DEV_USB :
		stat = 0; /* Assume ready */
		break;

	default:
		stat = STA_NOINIT;
	}
	return stat;
}

/*-----------------------------------------------------------------------*/
/* Initialize a Drive                                                    */
/*-----------------------------------------------------------------------*/

DSTATUS disk_initialize (
	BYTE pdrv				/* Physical drive number to identify the drive */
)
{
	DSTATUS stat;

	switch (pdrv) {
	case DEV_FLASH :
		stat = 0; /* Assume initialized */
		break;

	case DEV_MMC :
		stat = 0; /* Assume initialized */
		break;

	case DEV_USB :
		stat = 0; /* Assume initialized */
		break;

	default:
		stat = STA_NOINIT;
	}
	return stat;
}

/*-----------------------------------------------------------------------*/
/* Read Sector(s)                                                       */
/*-----------------------------------------------------------------------*/

DRESULT disk_read (
	BYTE pdrv,		/* Physical drive number to identify the drive */
	BYTE *buff,		/* Data buffer to store read data */
	LBA_t sector,	/* Start sector in LBA */
	UINT count		/* Number of sectors to read */
)
{
	DRESULT res;

	switch (pdrv) {
	case DEV_FLASH :
		/* Stub implementation */
		res = RES_OK;
		break;

	case DEV_MMC :
		/* Stub implementation */
		res = RES_OK;
		break;

	case DEV_USB :
		/* Stub implementation */
		res = RES_OK;
		break;

	default:
		res = RES_PARERR;
	}

	return res;
}

/*-----------------------------------------------------------------------*/
/* Write Sector(s)                                                      */
/*-----------------------------------------------------------------------*/

#if FF_FS_READONLY == 0

DRESULT disk_write (
	BYTE pdrv,			/* Physical drive number to identify the drive */
	const BYTE *buff,	/* Data to be written */
	LBA_t sector,		/* Start sector in LBA */
	UINT count			/* Number of sectors to write */
)
{
	DRESULT res;

	switch (pdrv) {
	case DEV_FLASH :
		/* Stub implementation */
		res = RES_OK;
		break;

	case DEV_MMC :
		/* Stub implementation */
		res = RES_OK;
		break;

	case DEV_USB :
		/* Stub implementation */
		res = RES_OK;
		break;

	default:
		res = RES_PARERR;
	}

	return res;
}

#endif

/*-----------------------------------------------------------------------*/
/* Miscellaneous Functions                                               */
/*-----------------------------------------------------------------------*/

DRESULT disk_ioctl (
	BYTE pdrv,		/* Physical drive number (0..) */
	BYTE cmd,		/* Control code */
	void *buff		/* Buffer to send/receive control data */
)
{
	DRESULT res;

	switch (pdrv) {
	case DEV_FLASH :
		switch (cmd) {
		case CTRL_SYNC :
			res = RES_OK;
			break;
		case GET_SECTOR_COUNT :
			*(LBA_t*)buff = 1024; /* Stub: 1024 sectors */
			res = RES_OK;
			break;
		case GET_SECTOR_SIZE :
			*(WORD*)buff = 512; /* 512 bytes per sector */
			res = RES_OK;
			break;
		case GET_BLOCK_SIZE :
			*(DWORD*)buff = 1; /* 1 sector per block */
			res = RES_OK;
			break;
		default:
			res = RES_PARERR;
		}
		break;

	case DEV_MMC :
		switch (cmd) {
		case CTRL_SYNC :
			res = RES_OK;
			break;
		case GET_SECTOR_COUNT :
			*(LBA_t*)buff = 1024; /* Stub: 1024 sectors */
			res = RES_OK;
			break;
		case GET_SECTOR_SIZE :
			*(WORD*)buff = 512; /* 512 bytes per sector */
			res = RES_OK;
			break;
		case GET_BLOCK_SIZE :
			*(DWORD*)buff = 1; /* 1 sector per block */
			res = RES_OK;
			break;
		default:
			res = RES_PARERR;
		}
		break;

	case DEV_USB :
		switch (cmd) {
		case CTRL_SYNC :
			res = RES_OK;
			break;
		case GET_SECTOR_COUNT :
			*(LBA_t*)buff = 1024; /* Stub: 1024 sectors */
			res = RES_OK;
			break;
		case GET_SECTOR_SIZE :
			*(WORD*)buff = 512; /* 512 bytes per sector */
			res = RES_OK;
			break;
		case GET_BLOCK_SIZE :
			*(DWORD*)buff = 1; /* 1 sector per block */
			res = RES_OK;
			break;
		default:
			res = RES_PARERR;
		}
		break;

	default:
		res = RES_PARERR;
	}

	return res;
}

/*-----------------------------------------------------------------------*/
/* Get current time for FatFs timestamps                                */
/*-----------------------------------------------------------------------*/

DWORD get_fattime (void)
{
	/* Return a fixed timestamp for now */
	/* Format: bit31:25=Year(0..127 from 1980), bit24:21=Month(1..12), bit20:16=Day(1..31) */
	/*         bit15:11=Hour(0..23), bit10:5=Minute(0..59), bit4:0=Second/2(0..29) */
	
	/* Example: 2025-01-01 12:00:00 */
	/* Year: 2025-1980=45, Month: 1, Day: 1, Hour: 12, Minute: 0, Second: 0 */
	return ((DWORD)(45 << 25)) | ((DWORD)(1 << 21)) | ((DWORD)(1 << 16)) | 
	       ((DWORD)(12 << 11)) | ((DWORD)(0 << 5)) | ((DWORD)(0 >> 1));
}