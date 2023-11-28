#!/bin/bash

DEST_DISK=$1
BACKUP_FILE=$2

gunzip -c $BACKUP_FILE.image.gz | dd conv=noerror,sync status=progress of=/dev/$DEST_DISK
