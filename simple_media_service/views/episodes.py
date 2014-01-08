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

from ..models import Episode
from ..models import DBSession as db

@register_model
class EpisodesModel(BaseCollectionViewModel):
    model_name = 'episodes'
    id_fields = {
        'id': ('api_episodes', ),
    }


@register_model
class EpisodeModel(BaseViewModel):
    model_name = 'episode'
    dbmodelCls = Episode

    fields = ('episode_id', 'name', 'year', 'watched', 'watched_date', )
    id_fields = {
        'id': ('api_episode', 'episode_id', ),
        'episodes': ('api_episodes', 'show_id', 'episode_id', ),
    }


@lift()
@view_defaults(route_name='api_episodes')
class EpisodesView(APIView):
    @view_provides('episodes')
    def _get(self):
        return db.query(Episode).filter_by(
            season_id=self.match.season_id).order_by(Episode.number).all(), {}

    @view_requires('episode')
    @view_provides('episode')
    def _post(self):
        episode = Episode(
            self.request.input_model.number,
            self.request.input_model.path,
            name=self.request.input_model.name,
            sha=self.request.input_mode.sha
        )
        db.add(episode)
        db.flush()
        return episode


@lift()
@view_defaults(route_name='api_episode')
class EpisodeView(APIView):
    @view_provides('episode')
    def _get(self):
        return Episode.get_by_id(self.match.episode_id)

    @view_requires('episode')
    @view_provides('episode')
    def _put(self):
        name = self.request.input_model.name
        number = self.request.input_model.number
        path = self.request.input_model.path
        sha = self.request.input_model.sha
        watched = self.request.input_model.watched
        episode = Episode.get_by_id(self.match.episode_id)
        episode.name = name
        episode.number = number
        episode.path = path
        episode.sha = sha
        episode.watched = watched
        db.flush()
        return episode
