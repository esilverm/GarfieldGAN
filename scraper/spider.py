import scrapy
import datetime


class GarfieldScraper(scrapy.Spider):
    name = "garfield"
    start_urls = ["http://pt.jikos.cz/garfield/1981/"]

    def parse(self, response):
        for comic in response.css("td > img"):
            # if the comic is a sunday comic, skip it
            if (
                not datetime.datetime.strptime(
                    comic.css("img::attr(alt)").get()[9:], "%d/%m/%Y"
                ).weekday()
                == 6
            ):
                yield {
                    "image": comic.css("img::attr(src)").get(),
                }
        # get the next page
        for links in response.css("a"):
            if links.css("a::text").get() == "Next month":
                yield response.follow(
                    links.css("a::attr(href)").get(), callback=self.parse
                )
