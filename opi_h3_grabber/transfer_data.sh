#!/bin/sh
MONITORDIR="/root/raw_video/"
inotifywait -m -e create -e moved_to --format '%w%f' "${MONITORDIR}" | while read NEWFILE
do
	echo " ${NEWFILE} has been created" 
	rsync -avzP ${NEWFILE} imatveev@10.33.21.232:~/video_rec/
	#scp ${NEWFILE} imatveev@10.33.21.232:~/video_rec/
	rm ${NEWFILE}
	done
