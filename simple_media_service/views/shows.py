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
from prism_rest import view_requires

from prism_rest import BaseViewModel
from prism_rest import BaseCollectionViewModel
from prism_rest import register_model

from ..models import Show
from ..models import DBSession as db

@register_model
class ShowsModel(BaseCollectionViewModel):
    model_name = 'shows'
    id_fields = {
        'id': ('api_shows', ),
    }


@register_model
class ShowModel(BaseViewModel):
    model_name = 'show'
    dbmodelCls = Show

    fields = ('show_id', 'name', )
    id_fields = {
        'id': ('api_show', 'show_id', ),
        'seasons': ('api_seasons', 'show_id', ),
    }


@lift()
@view_defaults(route_name='api_shows')
class ShowsView(APIView):
    @view_provides('shows')
    def _get(self):
        return db.query(Show).order_by(Show.name).all(), {}

    @view_requires('show')
    @view_provides('show')
    def _post(self):
        show = Show(self.request.input_model.name)
        db.add(show)
        db.flush()
        return show


@lift()
@view_defaults(route_name='api_show')
class ShowView(APIView):
    @view_provides('show')
    def _get(self):
        return Show.get_by_id(self.match.show_id)

    @view_requires('show')
    @view_provides('show')
    def _put(self):
        name = self.request.input_model.name
        show = Show.get_by_id(self.match.show_id)
        show.name = name
        db.flush()
        return show
