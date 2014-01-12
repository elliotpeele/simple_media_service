#
# Copyright (c) Elliot Peele <elliot@bentlogic.net>
#
# This program is distributed under the terms of the MIT License as found
# in a file called LICENSE. If it is not present, the license
# is always available at http://www.opensource.org/licenses/mit-license.php.
#
# This program is distributed in the hope that it will be useful, but
# without any warrenty; without even the implied warranty of merchantability
# or fitness for a particular purpose. See the MIT License for full details.
#

import os
import re
import hashlib
import logging

log = logging.getLogger('simple_media_service.client')

import prism_rest_client
from prism_rest_client.lib.util import AttrDict

class SMSClient(object):
    # Broadchurch.1x08.HDTVxx264-FoV.mp4
    # Broadchurch.S01E06.PROPER.HDTV.x264-TLA.mp4
    # Castle.2009.S06E08.HDTV.x264-LOL.mp4
    FILE_RE = re.compile('(.*)\.([Ss](\d+)[Ee](\d+)|(\d+)x(\d+))\..*')

    def __init__(self, uri):
        self.api = prism_rest_client.open(uri)
        self.shows = dict((x.name, x) for x in self.api.library.shows)

    def addfile(self, path):
        m = self.FILE_RE.match(os.path.basename(path))
        if not m:
            log.warn('skipping %s', path)
            return

        groups = m.groups()
        if not ((groups[2] and groups[3]) or (groups[4] and groups[5])):
            log.warn('didn\'t find season and episode: %s', path)
            return

        showsName = groups[0]
        seasonNum, episodeNum = groups[2], groups[3]
        if not seasonNum and not episodeNum:
            seasonNum, episodeNum = groups[4], groups[5]

        if showsName in self.shows:
            shows = self.shows.get(showsName)
        else:
            shows = self.api.library.shows.append({
                'name': showsName,
            })

        seasons = dict((int(x.name), x) for x in shows.seasons)
        if int(seasonNum) in seasons:
            season = seasons.get(int(seasonNum))
        else:
            season = shows.seasons.append({
                'name': str(int(seasonNum)),
            })

        episodes = dict((x.number, x) for x in season.episodes)
        if int(episodeNum) in episodes:
            episode = episodes.get(int(episodeNum))
        else:
            episode = season.episodes.append({
                'number': int(episodeNum),
                'path': path,
                'sha': self._calcSHA256(path),
            })

        log.info('episode added: %s', path)

        return episode

    def _calcSHA256(self, path):
        sha = hashlib.sha256()
        f = open(path)
        f.seek(0, 2)
        end = f.tell()
        f.seek(0)
        pos = 0
        part = 1024 * 1024 * 10
        while pos < end:
            if pos + part > end:
                part = end - pos
            sha.update(f.read(part))
            pos = f.tell()
        return sha.hexdigest()

    def addtree(self, root):
        for dirpath, dirnames, filenames in os.walk(root):
            for fname in filenames:
                if not fname.endswith('.mp4'):
                    continue
                yield self.addfile(os.path.join(root, dirpath, fname))
