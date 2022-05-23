# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime


def remove_white_spaces(text):
    # strip from tabs and spaces
    text = text.strip()
    return text

def extract_tag(text):
    #strip URL for tag only
    text = text[text.rfind("/")+1:]
    return text

def extract_channel(text):
    #strip URL for channel only and format the right name
    text = text[text.rfind("/")+1:].replace("-"," ").title()
    return text

def extract_date(text):
    #convert video date to python format
    return datetime.strptime(text,"%Y-%m-%d")


# should do some polishing on the output info
class VideoItem(Item):
    title = Field(
        input_processor=MapCompose(remove_white_spaces),
        output_processor=TakeFirst()
        )
    video_link = Field(
        output_processor=TakeFirst()

    )
    thumbnail = Field(
        output_processor=TakeFirst()

    )
    views = Field(
        output_processor=TakeFirst()

    )
    duration = Field(
        input_processor=MapCompose(remove_white_spaces),
        output_processor=TakeFirst()
    )
    author = Field(
        output_processor=TakeFirst()
    )
    comments_no = Field(
        output_processor=TakeFirst()

    )
    video_description = Field(
        input_processor=MapCompose(remove_white_spaces),
        output_processor=TakeFirst()

    )
    video_year = Field(
        input_processor = MapCompose(extract_date),
        output_processor = TakeFirst()

    )
    video_country = Field(
        output_processor=TakeFirst()

    )
    video_channels = Field(
    )

    video_tags = Field(
        input_processor=MapCompose(extract_tag)
    )

class ChannelItem(Item):
    title = Field(
        output_processor=TakeFirst()
    )
    image_url = Field(
        output_processor = TakeFirst()
    )
    description = Field(
        output_processor=TakeFirst()
    )