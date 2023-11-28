#!/bin/bash

SOURCE_DISK=$1
BACKUP_FILE=$2

dd if=/dev/$SOURCE_DISK conv=sync,noerror bs=64K | gzip -c > $BACKUP_FILE.image.gz
