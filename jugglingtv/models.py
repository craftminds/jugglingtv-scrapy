
from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


# Association Table for Many-to-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
quote_tag = Table('video_tag', Base.metadata,
    Column('video_id', Integer, ForeignKey('video.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Video(Base):

    __tablename__ = "video"

    id = Column(Integer, primary_key=True)
    title = Column('title', Text())
    thumbnail_url = Column('thumbnail_url', String(2048))
    video_url = Column('video_url', String(2048))
    views = Column('views', Integer)
    duration = Column('duration', Integer)
    comments_no = Column('comments_no', Integer)
    description = Column('description', Text())
    year = Column('year', Integer)
    country = Column('country', String(20))
    author_id = Column(Integer, ForeignKey('author.id'))  # Many videos to one author
    tags = relationship('Tag', secondary='video_tag',
        lazy='dynamic', backref="video")  # M-to-M for quote and tag


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    videos = relationship('Video', backref='author')  # One author to many Videos


class Tag(Base):
    __tablename__ = "tag"

    #M-to-M for tag and video

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True)
    quotes = relationship('Video', secondary='video_tag',
        lazy='dynamic', backref="tag")  # M-to-M for quote and tag
