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

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import ForeignKey

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class BaseResource(object):
    creation_date = Column(DateTime, default=datetime.utcnow)
    modification_date = Column(DateTime, onupdate=datetime.utcnow)

    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter_by(**{
            '%s_id' % cls.__name__.lower(): id}).first()

    @classmethod
    def get_all(cls):
        return DBSession.query(cls).all()


class Show(BaseResource, Base):
    __tablename__ = 'shows'

    show_id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)

    def __init__(self, name):
        self.name = name


class Season(BaseResource, Base):
    __tablename__ = 'seasons'

    season_id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    year = Column(Integer)

    show_id = Column(Integer, ForeignKey(Show.show_id), index=True)
    show = relationship(Show, backref=backref('seasons', uselist=True))

    def __init__(self, name, year=None):
        self.name = name
        if year:
            self.year = year


class Episode(BaseResource, Base):
    __tablename__ = 'episodes'

    episode_id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    number = Column(Integer, nullable=False)
    path = Column(String, nullable=False)
    sha = Column(String(64))

    watched_date = Column(DateTime)

    season_id = Column(Integer, ForeignKey(Season.season_id), index=True)
    season = relationship(Season, backref=backref('seasons', uselist=True))

    def __init__(self, number, path, name=None, sha=None):
        self.number = number
        self.path = path
        if name:
            self.name = name
        if sha:
            self.sha = sha

    def _get_watched(self):
        return bool(self.watched_date)

    def _set_watched(self, val):
        if val:
            self.watched_date = datetime.utcnow
        else:
            self.watched_date = None

    watched = property(_get_watched, _set_watched)


class Device(BaseResource, Base):
    __tablename__ = 'devices'

    device_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ipaddr = Column(String, nullable=False)

    def __init__(self, name, ipaddr):
        self.name = name
        self.ipaddr = ipaddr


class Job(BaseResource, Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True)



