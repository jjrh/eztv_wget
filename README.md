Wget EZTV Torrents
=========================

About
-----

This program connects to eztv.it RSS feed and downloads the torrents of shows
listed in the 'shows.txt'

It was created because I would want to download a show that was released after
I had gone to bed to watch the next morning.

Files
-----
 - `eztv_wget.py` - The main program.
 - `.info_hashes` - file that contains the info hashes so torrents are not
   downloaded twice.
 - `shows.txt` - list of shows you want to look for.
    - one name per line.
    - show names don't have to be exact. The program does 'for showname in
      fullshowname' so putting 'bbc' in will download everything with bbc in
      the title.

 - `fetch.sh` -
    1. Bash script that runs the program, downloads new torrents.
    2. Moves the .torrent files to the torrent watch directory. In my case, I
       have a folder called `~/torrent_watch` which my client auto adds any
       torrents in that folder.

 - `notify.sh` -
    - A script that simply downloads any new torrents and notifies of the
      contents of the torrents directory.

 - `log/`
    - `clearLog.sh` - clears all the log files.
    - `detailed.txt` - verbose logging of found match URLs.
    - `simple.txt` - less verbose logging.

 - `torrents/` - Directory for storing downloaded .torrent files
    - `clear_torrents.sh` - clears all the torrent files.

Installing
----------
### Requirements:
 - Python
 - feedparser module (`sudo apt-get install python-feedparser`)

All that really needs to be done is to run `python eztv_wget.py`
For things to work nicely, a cronjob should be made.

In my case, I do:

    */15   *   *   *   *   ~/wget_rss/wget_torrents.sh

(Note: run `crontab -e` and put this in )

I run this every 15 minutes, but running every hour or what ever works fine.

Bash scripts will need to be modified to suit different setups, the
program will most likely not work with out this.

TODO
----
- Take out logging or add clear_logs to a cronjob. After ~24 hours
because of how I was reading the file into python I was running out of
memory and the program was crashing. doing fseek on the file and
writing there would be a much better way all together.
Over all how we log what we log should be done in a much more
intelligent way.

- Deal with websites that sometimes are linked that require one to visit
the site and download the torrent. (very annoying since wget won't work)
kickass torrents is the usual one.

