#!/usr/bin/env python
import feedparser
import time
import urllib2
import libtorrent as lt
import shutil
import tempfile

class Eztv(object):
    """Eztv torrent search"""

    # Version of this client
    VERSION = '0.8'

    # Path to RSS feed URI
    eztv_rss_link = "https://eztv.ag/ezrss.xml"

    # Path to the log directory
    log_path = 'log/'

    # Path to file containing the info_hashes from previous sessions
    info_hashes_filename = '.info_hashes'

    # List of already fetched torrent URLs
    info_hashes = []

    # List of shows to be downloaded
    target_shows = []

    # Detailed results
    results_detailed = []

    # Simple results
    results_simple = []

    # Storage for resulting torrent meta-data
    torrents = {}

    def __init__(self):
        """Constructor"""
        self.read_info_hashes(self.info_hashes_filename)

    def read_target_shows(self, filename):
        """Read the target shows from a file and populate target_shows list"""
        f = open(filename)
        for line in f:
            line = line.strip()
            if len(line):
                self.target_shows.append(line.upper())
        f.close()

    def read_info_hashes(self, filename):
        """Read the info_hashes file and populate the list"""
        try:
            f = open(filename)
        except IOError:
            # If we can't read it, move along, first time use probably
            return False

        for line in f:
            line = line.strip()
            if len(line):
                self.info_hashes.append(line)
        f.close()

    def parse_feed(self):
        """Parse the RSS feed"""
        return feedparser.parse(self.eztv_rss_link)

    def find_shows(self, target_shows_filename):
        """Find torrent links for shows in target_shows list"""
        self.read_target_shows(target_shows_filename)

        eztv_feed = self.parse_feed()

        for entry in eztv_feed.entries:
            for show in self.target_shows:
                if show.upper() in entry.title.upper():
                    torrent_uri = entry.enclosures[0].href
                    try:
                        # Try to get the infohash for a unique id
                        info_hash = entry.torrent_infohash
                        name = entry.torrent_filename
                    except:
                        info_hash,name = self.get_torrent_infohash(torrent_uri)
                        if info_hash == False:
                            # default to entry id as unique id if no infohash
                            info_hash = entry.id

                    if info_hash in self.info_hashes:
                        continue

                    self.info_hashes.append(info_hash)

                    if name == '':
                        # When the name is not read properly, we should default
                        # to the title
                        name = str(entry.title)

                    torrent = {
                        'info_hash': str(info_hash),
                        'name': name,
                        'uri': torrent_uri,
                        'title': entry.title
                    }

                    # Store each torrent by actual info_hash to eliminate duplicates
                    self.torrents[str(info_hash)] = torrent

        for ih in self.torrents:
            t = self.torrents[ih]
            self.results_detailed.append(t['info_hash']\
                    + " title: " + t['title']\
                    + " url: " + t['uri']\
                    + " name: " + t['name'])
            if t['uri'][0:7] == 'magnet:':
                # We got this far and it is a magnet link, we need to bail
                # since we cannot fetch the link
                self.results_detailed.append('# Skipping torrent because cannot download magnet link')
                self.results_simple.append(t['title'] + ' [SKIPPED]')
                continue
            else:
                self.results_simple.append(t['title'])

            # Now save the torrents to disk for later use
            savefile = 'torrents/' + t['name'] + '.torrent'
            self.save_file_from_url(t['uri'], savefile)

        self.write_logs()
        return len(self.torrents)

    def save_file_from_url(self, uri, filename):
        request = urllib2.Request(
            uri, 
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
            }
        )
        response = urllib2.urlopen(request)
        filedata = response.read()

        f = open(filename, 'w+')
        f.write(filedata)
        f.close()

    def get_torrent_infohash(self, uri):
        """Read the info_hash and name for a torrent URI"""
        if uri[0:7] == 'magnet:':
            # Getting an error when attempting to read magnet links so skipping
            # for now
            return False, uri
            info = self.read_magnet_torrent(uri)
        else:
            info = self.read_torrent(uri)

        if info == None:
            return False, ''

        return info.info_hash(), info.name()
    
    def read_torrent(self, torrent_uri):
        """Read the torrent_info for a given torrent URI"""
        tpointer,torrentfile = tempfile.mkstemp()
        self.save_file_from_url(torrent_uri, torrentfile)
        torrent = open(torrentfile, 'rb').read()
        e = lt.bdecode(torrent)
        if e == None:
            return None
        info = lt.torrent_info(e)
        return info

    def read_magnet_torrent(self, magnet_uri):
        """Read the torrent_info from a given magnet torrent"""
        params = {
            'save_path': '.',
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': True,
            'duplicate_is_error': True
        }

        handle = lt.add_magnet_uri(lt.session(), magnet_uri, params)
        while (not handle.has_metadata()):
           time.sleep(.1)
        info = handle.get_torrent_info()
        return info

    def write_logs(self):
        """Write data to log files"""
        # Preserve existing content in these logs
        self.save_list(self.log_path + 'simple.txt', self.results_simple, 'a')
        self.save_list(self.log_path + 'detailed.txt', self.results_detailed, 'a')

        # Overwrite this log
        self.save_list(self.info_hashes_filename, self.info_hashes, 'w')

    def save_list(self, filename, data_list, mode):
        """Write list of data to a log file"""
        f = open(filename, mode)

        for item in data_list:
            f.write(item + '\n')

        f.close()

if __name__ == "__main__":
    eztv = Eztv()
    results_count = eztv.find_shows('shows.txt')
    if results_count:
        print "+---------------------------------"
        print "| " + str(results_count) + " New Torrents! "
        print "+---------------------------------"

        i = 1
        for result in eztv.results_simple:
            print " " + str(i) + ".  " + result.strip()
            i += 1
