# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def remove_white_spaces(text):
    # strip from tabs and spaces
    text = text.re("[^\t\n]+")
    return text

# should do some polishing on the output info
class VideoItem(Item):
    title = Field(
        input_processor=MapCompose(remove_white_spaces),
        output_processor=TakeFirst()
        )
    video_link = Field()
    thumbnail = Field()
    views = Field()
    duration = Field()
    author = Field()
    comments_no = Field()
    video_description = Field()
    video_year = Field()
    video_country = Field()
    video_channels = Field()
    video_tags = Field()
   
    


# continue here:https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-ii-b917509b73f7



