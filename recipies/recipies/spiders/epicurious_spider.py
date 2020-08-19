import scrapy


class Epicurious(scrapy.Spider):
    name = "epicurious"

    url = 'https://www.epicurious.com/search/?content=recipe&page='
    
    start_urls = ["https://www.epicurious.com/search/?content=recipe&page="
    +str(num+1) for num in range(2028)]


    #called parse because def callback
    def parse(self, response):
        for next_page in response.css(".view-complete-item::attr(href)").extract():
            yield response.follow(next_page,callback=self.parse_recipie)
    
    def parse_recipie(self, response):
        review = response.css(".review-text p::text").extract()
        ings = response.css(".ingredient::text").extract()
        dish = response.css(".title-source h1::text").extract()[0]
        yield {
            'dish' : dish.strip(),
             'ingredients' : ("; ").join(ings),
              'reviews' : review
              }