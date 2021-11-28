### Introduction

This is the place to scrap all the data from juggling.tv. First step to create mobile app to browse the videos on you smartphone.

### Links to gather data

To be used later in the spider program:

- Title (list): response.css('table.title a::text').re("[^\t\n]+")
- Video link: response.css('table.title a::attr(href)').get()
- Thumbnail link: response.css('div.imagewatch img::attr(src)').get()
- Views: response.css('td.views::text').get()
- Duration (list): response.css('td.duration::text').re("[^\t\n]+")
- Author: response.css('td.by a::text').get()
- Comments: response.css('td.comments::text').get()

### Commands to run spiders:
```python
scrapy crawl author -O videos.json 
```
-O moderator overwrites the output file

### TODO:
- [ ] create the spider to go through all the webpages with thumbnails
- [ ] visit all video pages and gather even more data!