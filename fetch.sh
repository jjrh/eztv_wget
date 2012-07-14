#!/bin/bash
TORRENTDIR=~/torrent_folder

if [ ! -d "$TORRENTDIR" ]; then
    mkdir "$TORRENTDIR"
fi

# Get the full path where this script lives
DIR=$( cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd $DIR

echo "Searching for shows:"
cat shows.txt
python eztv_wget.py

mv torrents/*.torrent "$TORRENTDIR"
