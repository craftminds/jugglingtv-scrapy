import scrapy
from jugglingtv.items import VideoItem
from scrapy.loader import ItemLoader


import logging


# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)

class AuthorSpider(scrapy.Spider):
    name = 'videos'
    video_item = VideoItem()
    start_urls = ['http://juggling.tv/videos/basic/mr']
    
    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))
        videos = response.css("div.listwatch")
        for video in videos:
            loader = ItemLoader(item=VideoItem(), selector = video)
            loader.add_css('title', 'table.title a::text')
            # loader.add_css('video_link', 'video::attr(src)')
            loader.add_css('thumbnail', 'div.imagewatch img::attr(src)')
            loader.add_css('views', 'td.views::text')
            loader.add_css('duration', 'td.duration::text')
            loader.add_css('author', 'td.by a::text')
            loader.add_css('comments_no', 'td.comments::text')
            video_item = loader.load_item()
                
            # get inside the video and extract data
            video_url = video.css('table.title a::attr(href)').get()
            yield response.follow(video_url, self.parse_single_video, meta={'video_item': video_item})
        # next_page = response.css('a.rightPaging::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
    
    def parse_single_video(self, response):
        # def extract_with_css(query):
        #     return response.css(query).get(default='').strip()
       video_item = response.meta['video_item']
       loader = ItemLoader(item=video_item, response = response)
       loader.add_css('video_description', 'div.vv-video-desc::text')
       loader.add_css('video_year', 'span.vv-date::text')
       loader.add_css('video_country', 'span.vv-cunt::text')
       loader.add_css('video_link', 'video::attr(src)')
       loader.add_css('video_channels', 'div.mb-5.vv-chan a::attr(href)')
       loader.add_css('video_tags', 'div.mb-5.vv-tags a::attr(href)')
       # this function is a key to run the item loader, otherwise there was no output
       yield loader.load_item()
 

       