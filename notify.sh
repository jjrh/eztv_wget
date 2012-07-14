#!/bin/bash

# Get the full path where this script lives
DIR=$( cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd $DIR

python eztv_wget.py

notify-send 'eztv-wget' "`ls torrents/*.torrent`"
