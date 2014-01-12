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

from ..models import Season
from ..models import DBSession as db

@register_model
class SeasonsModel(BaseCollectionViewModel):
    model_name = 'seasons'
    id_fields = {
        'id': ('api_seasons', 'show_id', ),
    }


@register_model
class SeasonModel(BaseViewModel):
    model_name = 'season'
    dbmodelCls = Season

    fields = ('season_id', 'name', 'year', )
    id_fields = {
        'id': ('api_season', ('show_id', 'season_id', ), ),
        'show': ('api_show', ('show_id', ), ),
        'episodes': ('api_episodes', ('show_id', 'season_id', ), ),
    }


@lift()
@view_defaults(route_name='api_seasons')
class SeasonsView(APIView):
    @view_provides('seasons')
    def _get(self):
        return db.query(Season).filter_by(show_id=self.match.show_id).order_by(
            Season.name).all(), {}

    @view_requires('season')
    @view_provides('season')
    def _post(self):
        season = Season(
            self.request.input_model.name,
            self.request.input_model.year,
        )
        season.show_id = self.match.show_id
        db.add(season)
        db.flush()
        return season


@lift()
@view_defaults(route_name='api_season')
class SeasonView(APIView):
    @view_provides('season')
    def _get(self):
        return Season.get_by_id(self.match.season_id)

    @view_requires('season')
    @view_provides('season')
    def _put(self):
        name = self.request.input_model.name
        year = self.request.input_model.year
        season = Season.get_by_id(self.match.season_id)
        season.name = name
        season.year = year
        db.flush()
        return season
