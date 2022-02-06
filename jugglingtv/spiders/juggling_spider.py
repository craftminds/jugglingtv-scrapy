import scrapy
from jugglingtv.items import VideoItem
from scrapy.loader import ItemLoader




class AuthorSpider(scrapy.Spider):
    name = 'author'
    video_item = VideoItem()

    start_urls = ['http://juggling.tv/videos/basic/mr']

    def parse(self, response):
        for video in response.css("div.listwatch"):
            loader = ItemLoader(item=VideoItem(), selector = video)
            loader.add_css('title', 'table.title a::text')
            loader.add_css('video_link', 'table.title a::attr(href)')
            video_item = loader.load_item()
                #  'title': video.css('table.title a::text').re("[^\t\n]+")[0],
                # 'video_link': video.css('table.title a::attr(href)').get(),
                # 'thumbnail': video.css('div.imagewatch img::attr(src)').get(),
                # 'views': video.css('td.views::text').get(),
                # 'duration': video.css('td.duration::text').re("[^\t\n]+")[0],
                # 'author': video.css('td.by a::text').get(),
                # 'comments_no': video.css('td.comments::text').get(),

            # get inside the video and extract data
            video_url = video.css('table.title a::attr(href)').get()
            yield response.follow(video_url, self.parse_single_video, meta={'video_item': video_item})

        next_page = response.css('a.rightPaging::attr(href)').get()
        if next_page is not 'http://juggling.tv/videos/basic/mr/3':
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def parse_single_video(self, response):
        # def extract_with_css(query):
        #     return response.css(query).get(default='').strip()
       video_item = response.meta['video_item']
       loader = ItemLoader(item=video_item, response = response)
       loader.add_css('video_description', 'div.vv-video-desc::text')
       loader.add_css('video_year', 'span.vv-loco::text')
       loader.add_css('video_country', 'span.vv-cunt::text')
       loader.add_css('video_channels', 'div.mb-5.vv-chan a::attr(href)')
       loader.add_css('video_tags', 'div.mb-5.vv-tags a::attr(href)')

       