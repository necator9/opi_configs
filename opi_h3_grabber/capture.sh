#!/bin/bash

t=1
while [ $t -le 300 ]
do
	name='/root/raw_video/vid_$t.mp4'
	ffmpeg -i 'rtsp://192.168.1.10/user=admin&password=&channel=1&stream=0.sdp?Real_stream' -fs 1000M -c copy -y $name
	rsync -avzP $name imatveev@10.33.21.232:~/raw_video/
	rm $name
	t=`expr $t + 1`
done
