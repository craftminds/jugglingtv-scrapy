# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from jugglingtv.models import Video, Author, Tag, db_connect, create_table

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
        video.title = item["title"]
        video.thumbnail_url = item["thumbnail"]
        video.video_url = item["video_link"]
        video.views = item["views"]
        video.duration = item["duration"]
        video.comments_no = item["comments_no"]
        video.description = item["video_description"]
        video.year = item["video_year"]
        try:
            video.country = item["video_country"]
        except KeyError:
            video.country = ''
        author.name = item["author"]
        # tag.name = item["video_tags"]

        # check whether the author exists
        exist_author = session.query(Author).filter_by(name = author.name).first()
        if exist_author is not None:  # the current author exists
            video.author = exist_author
        else:
            video.author = author

        # check whether the current video has tags or not
        if "tags" in item:
            for tag_name in item["video_tags"]:
                tag = Tag(name=tag_name)
                # check whether the current tag already exists in the database
                exist_tag = session.query(Tag).filter_by(name = tag.name).first()
                if exist_tag is not None:  # the current tag exists
                    tag = exist_tag
                video.tags.append(tag)

        try:
            session.add(video)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item