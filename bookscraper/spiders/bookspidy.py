import scrapy


class BookspidySpider(scrapy.Spider):
    name = "bookspidy"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        books=response.css('article.product_pod')
        for book in books:
           

            relative_url=book.css('h3 a::attr(href)').get()
            if 'catalogue/' in relative_url:
                book_url="http://books.toscrape.com/"+relative_url
            else:
                book_url="http://books.toscrape.com/catalogue/"+relative_url
            yield response.follow(book_url,callback=self.parse_nextpage)
            next_page=response.css('li.next a::attr(href)').get()
            
            if next_page is not None:
                if 'catalogue/' in next_page:
                    next_page_url="http://books.toscrape.com/"+next_page
                else:
                    next_page_url="http://books.toscrape.com/catalogue/"+next_page
                yield response.follow(next_page_url,callback=self.parse)
    def parse_nextpage(self,response):
        table_row=response.css("table tr")
        yield{
            "name":response.css('.product_main h1::text').get(),
            "price":response.css('.product_main h1::text').get(),
            "product_description": response.xpath("/html/body/div[1]/div/div[2]/div[2]/article/p/text()").get(),
            "Number of reviews":table_row[(len(table_row)-1)].css('td::text').get()

        }
        