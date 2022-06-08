import scrapy
from jugglingtv.items import VideoItem, ChannelItem, AuthorItem
from scrapy.loader import ItemLoader


import logging


# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)

class AuthorSpider(scrapy.Spider):
    name = 'videos'
    video_item = VideoItem()
    start_urls = ['http://juggling.tv/videos/basic/mr']
    # individual pipeline for every spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'jugglingtv.pipelines.SaveVideosPipeline': 300,
        }
    }
    
    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))
        videos = response.css("div.listwatch")
        for video in videos:
            loader = ItemLoader(item=VideoItem(), selector = video)
            loader.add_css('title', 'table.title a::text')
            #loader.add_css('video_link', 'video::attr(src)')
            loader.add_css('thumbnail', 'div.imagewatch img::attr(src)')
            loader.add_css('views', 'td.views::text')
            loader.add_css('duration', 'td.duration::text')
            loader.add_css('author', 'td.by a::text')
            loader.add_css('comments_no', 'td.comments::text')
            video_item = loader.load_item()
                
            # get inside the video and extract data
            video_url = video.css('table.title a::attr(href)').get()
            yield response.follow(video_url, self.parse_single_video, meta={'video_item': video_item})
        # step to another page from here
        next_page = response.css('a.rightPaging::attr(href)').get()
        if next_page is not None:
           # self.logger.info('Go to another page')
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def parse_single_video(self, response):
        # def extract_with_css(query):
        #     return response.css(query).get(default='').strip()
       video_item = response.meta['video_item']
       loader = ItemLoader(item=video_item, response = response)
       loader.add_css('video_description', 'div.vv-video-desc::text')
       loader.add_css('video_year', 'span.vv-date::text')
       loader.add_css('video_country', 'span.vv-cunt::text')
       loader.add_css('video_channels', 'div.mb-5.vv-chan a::text')
       loader.add_css('video_tags', 'div.mb-5.vv-tags a::attr(href)')
       loader.add_css('video_link', 'video::attr(src)')
       # this function is a key to run the item loader, otherwise there was no output
       yield loader.load_item()

class ChannelSpider(scrapy.Spider):
    name = 'channels'
    channel_item = ChannelItem()
    start_urls = ['http://juggling.tv/channels']
    # individual pipeline for every spider
    custom_settings = {
        'ITEM_PIPELINES': {
            'jugglingtv.pipelines.SaveChannelsPipeline': 300,
        }
    }

    def parse(self,response):
        channels_type = response.css("div.listchannel")
        for channel in channels_type:
            self.logger.info('Scrape it!')
            loader = ItemLoader(item=ChannelItem(), selector = channel)
            # title
            loader.add_css('title', 'h2.title ::text')
            # image URL
            loader.add_css('image_url', 'div.imagechannel img::attr(src)')
            # description
            loader.add_css('description', 'span.chan_desc::text')
            channel_item = loader.load_item()
            yield loader.load_item()

class AuthorSpider(scrapy.Spider):
    name = 'authors'
    author_item = AuthorItem()
    start_urls = ['http://juggling.tv/members']
    custom_settings = {
        'ITEM_PIPELINES': {
            'jugglingtv.pipelines.SaveAuthorsPipeline': 300,
        }
    }

    def parse(self,response):
        authors = response.css("div.listmember")
        for author in authors:
            # self.logger.info('Scrape authors!')

            # test and scare for authors below
            loader = ItemLoader(item=AuthorItem(), selector = author)
            # title
            loader.add_css('name', 'div.membername ::text')
            # image URL
            loader.add_css('image_url', 'img::attr(src)')
            author_item = loader.load_item()

            # get inside the author and extract data
            author_url = author.css('a::attr(href)').get()
            #yield loader.load_item()
            yield response.follow(author_url, self.parse_single_author, meta={'author_item': author_item})
        #step to another page 
        next_page = response.css('a.rightPaging::attr(href)').get()
        if next_page is None:
           # self.logger.info('Go to another page')
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def parse_single_author(self, response):
        author_item = response.meta['author_item']
        loader = ItemLoader(item=author_item, response = response)

        # get the list of headers and strip from whitespaces
        profile_info_headers = response.css('h3.field-name-profile ::text').getall()
        profile_info_headers = [i.strip(': ') for i in profile_info_headers]
        print(profile_info_headers)
        # get the list of profile info and strip from whitespaces
        profile_info_list = response.css('div.profileinfo ::text').getall()
        profile_info_list = [i.strip() for i in profile_info_list]

        
        print(profile_info_list)
   
        # check if the full name is there
        full_name = response.css('div.field-name-profile ::text').get()


        if full_name is None:
            # full_name = response.css('div.profileinfo::text').get().strip()
            loader.add_value('full_name', ' ')
            profile_info_dict = dict(zip(profile_info_headers,profile_info_list))
        else:
            loader.add_value('full_name', profile_info_list[0])
            profile_info_headers.insert(0, 'Full name')
            profile_info_dict = dict(zip(profile_info_headers,profile_info_list))
        
        # loader.add_css('no_followers', )
        if 'Followers' in profile_info_dict:
            loader.add_value('no_followers', profile_info_dict['Followers'])
        else:
            loader.add_value('no_followers', 0)
        # loader.add_css('video_views', )
        # loader.add_css('profile_views', )
        # loader.add_css('profileinfo_url', )
        yield loader.load_item()

