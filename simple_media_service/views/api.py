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

from prism_core.views import lift
from prism_core.views import view_defaults

from prism_rest import APIView
from prism_rest import view_provides

from prism_rest import BaseViewModel
from prism_rest import register_model


@register_model
class ApiModel(BaseViewModel):
    model_name = 'api'
    static_model = True
    id_fields = {
        'id': ('api', ),
        'library': ('api_library', ),
    }


@lift()
@view_defaults(route_name='api')
class Api(APIView):
    @view_provides('api')
    def _get(self):
        return {}
