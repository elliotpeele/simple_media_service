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

from pyramid.response import Response

from prism_core.views import lift
from prism_core.views import BaseView
from prism_core.views import view_defaults

@lift()
@view_defaults(route_name='home', renderer='text')
class Home(BaseView):
    def _get(self):
        return Response('UI goes here')
