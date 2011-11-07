#!/bin/bash
python eztv_wget.py
for k in  $(cat /log/wget.txt)
do
	wget "$k"
done
mv *.torrent ~/torrent_folder 2> /dev/null
echo "" > /log/wget.txt

