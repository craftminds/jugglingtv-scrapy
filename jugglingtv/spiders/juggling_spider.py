import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

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

        next_page = response.css('a.rightPaging::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)