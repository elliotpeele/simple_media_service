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
import sys
import epdb
sys.excepthook = epdb.excepthook()

from pyramid.paster import setup_logging

from ..client import SMSClient

import logging
log = logging.getLogger('simple_media_service.scripts.add_tree')
log.setLevel(logging.DEBUG)

def usage(argv):
    cmd = os.path.basename(argv[0])
    print 'usage: %s <config_uri> <service_uri> <file_path>' % cmd
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 4:
        usage(argv)
    config_uri = argv[1]
    service_uri = argv[2]
    file_path = argv[3]
    setup_logging(config_uri)

    client = SMSClient(service_uri)
    for episode in client.addtree(file_path):
        if not episode:
            continue
        log.info('indexed %s - Season %s - Episode %s',
            episode.season.show.name, episode.season.name, episode.number)
