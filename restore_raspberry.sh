#!/bin/bash

SOURCE_DISK=$1
BACKUP_FILE=$2

dd if=/dev/$SOURCE_DISK conv=noerror,sync status=progress bs=1M | gzip -c > $BACKUP_FILE.image.gz
