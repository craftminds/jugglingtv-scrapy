import scrapy
from jugglingtv.items import VideoItem
from scrapy.loader import ItemLoader




class AuthorSpider(scrapy.Spider):
    name = 'author'
    # video_item = VideoItem()

    start_urls = ['http://juggling.tv/videos/basic/mr']

    def parse(self, response):
        for video in response.css("div.listwatch"):
            yield {
                'title': video.css('table.title a::text').re("[^\t\n]+")[0],
                'video_link': video.css('table.title a::attr(href)').get(),
                'thumbnail': video.css('div.imagewatch img::attr(src)').get(),
                'views': video.css('td.views::text').get(),
                'duration': video.css('td.duration::text').re("[^\t\n]+")[0],
                'author': video.css('td.by a::text').get(),
                'comments_no': video.css('td.comments::text').get(),
            }
            video_url = video.css('table.title a::attr(href)').get()
            self.logger.info('get video page url')
            self.logger.info(video_url)
            yield response.follow(video_url, callback = self.parse_single_video)

        next_page = response.css('a.rightPaging::attr(href)').get()
        if next_page is 'http://juggling.tv/videos/basic/mr/3':
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def parse_single_video(self, response):
        # def extract_with_css(query):
        #     return response.css(query).get(default='').strip()
        
        yield {
            'video_title':response.css('h3.vv-video-title::text').get(),
        }

