# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from jugglingtv.models import Video, Author, Tag, Channel, db_connect, create_table

# class JugglingtvPipeline:
#     def process_item(self, item, spider):
#         return item

class SaveVideosPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Save videos in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        video = Video()
        author = Author()
        tag = Tag()
        channel = Channel()
        video.title = item["title"]
        video.thumbnail_url = item["thumbnail"]
        video.video_url = item["video_link"]
        video.views = item["views"]
        video.duration = item["duration"]
        video.comments_no = item["comments_no"]
        video.description = item["video_description"]
        video.year = item["video_year"]
        
        #check whether video_country exists
        if "video_country" in item:
            video.country = item["video_country"]
        else:
            video.country = ''
        
        author.name = item["author"]

        # check whether the author exists
        exist_author = session.query(Author).filter_by(name = author.name).first()
        if exist_author is not None:  # the current author exists
            video.author = exist_author
        else:
            video.author = author

        # check whether the current video has tags or not
        if "video_tags" in item:
            for tag_name in item["video_tags"]:
                tag = Tag(name=tag_name)
                # check whether the current tag already exists in the database
                exist_tag = session.query(Tag).filter_by(name = tag.name).first()
                if exist_tag is not None:  # the current tag exists
                    tag = exist_tag
                video.tags.append(tag)
        
        # check whether the current video has channels or not
        if "video_channels" in item:
            for channel_name in item["video_channels"]:
                channel = Channel(name=channel_name)
                # check whether the current tag already exists in the database
                exist_channel = session.query(Channel).filter_by(name = channel.name).first()
                if exist_channel is not None:  # the current tag exists
                    channel = exist_channel
                video.channels.append(channel)

        try:
            session.add(video)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

class SaveChannelsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Save videos in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        channel = Channel()
        
        #check if the name exist
        channel = Channel(name=item["title"])
        exist_channel = session.query(Channel).filter_by(name = channel.name).first()
        #UPDATE if exist.
        if exist_channel is not None:
            exist_channel.image_url = item["image_url"]
            exist_channel.description = item["description"]
        #ADD if doesn't exist
        else:
            channel.name = item["title"]
            channel.image_url = item["image_url"]
            channel.description = item["description"]
            session.add(channel)

        try:
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

class SaveAuthorsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Save authors in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        author = Author()
        
        #check if the name exist
        author = Author(name=item["title"])
        exist_author = session.query(Author).filter_by(name = channel.name).first()
        #UPDATE if exist.
        if exist_author is not None:
            
            exist_author.image_url = item["image_url"]
            exist_author.description = item["description"]
            exist_author.full_name = item["full_name"]
            exist_author.no_followers = item["no_followers"]
            exist_author.video_views = item["video_views"]
            exist_author.profile_views = item["profile_views"]
            exist_author.profileinfo_url = item["profileinfo_url"]   
        #ADD if doesn't exist
        else:
            author.name = item["title"]
            author.image_url = item["image_url"]
            author.description = item["description"]
            author.full_name = item["full_name"]
            author.no_followers = item["no_followers"]
            author.video_views = item["video_views"]
            author.profile_views = item["profile_views"]
            author.profileinfo_url = item["profileinfo_url"]

            session.add(author)

        try:
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
    