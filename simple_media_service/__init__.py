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

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import Base
from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('prism_rest')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('api',             '/api')
    config.add_route('api_library',     '/api/library')
    config.add_route('api_shows',       '/api/library/shows')
    config.add_route('api_show',        '/api/library/shows/{show_id}')
    config.add_route('api_seasons',     '/api/library/shows/{show_id}/seasons')
    config.add_route('api_season',      '/api/library/shows/{show_id}/seasons/{season_id}')
    config.add_route('api_episodes',    '/api/library/shows/{show_id}/seasons/{season_id}/episodes')
    config.add_route('api_episode',     '/api/library/shows/{show_id}/seasons/{season_id}/episodes/{episode_id}')

    config.scan()
    return config.make_wsgi_app()
