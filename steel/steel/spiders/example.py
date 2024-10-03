import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["tnmk-murmansk.ru"]
    start_urls = [f"https://tnmk-murmansk.ru/polosa-metallicheskaya?page={i}" for i in range(1, 1029)]

    def parse(self, response):
        heads = response.xpath('//div[@class="product-line-list"]/div[@class="js-product-item product-line"]')
        for head in heads:
            link = 'https://tnmk-murmansk.ru' + head.xpath('.//p[@class="product-text"]/a/@href').get()
            yield scrapy.Request(url=link, callback=self.parse_product)

    def parse_product(self, response):
        # Извлечение информации с карточки товара
        title = response.xpath('//h1[@itemprop="name"]/text()').get().strip()
        # all_price = response.xpath('//span[@class="price-text"]/text()').get().strip() #Примерный селектор для цены
        photo = 'https://tnmk-murmansk.ru' + response.xpath('//img[@class="card-slider__img"]/@src').get().strip()
        try:
            params = response.xpath('//span[@class="price-text"]')
            all_price = params[0].xpath('.//text()').get().strip()
            wight = params[1].xpath('.//text()').get().strip()
            one_price = params[2].xpath('.//text()').get().strip()
        except:
            all_price = 'None'
            wight = 'None'
            one_price = 'Цена за тонну: ' + response.xpath(
                './/span[@class="price-text editable"]/text()').get().strip()
        glavki = response.xpath('//ul[@class="oglavl"]/li')
        get_params = []
        for glav in glavki:
            key = glav.xpath('.//span[@class="text"]/text()').get().strip()
            value = glav.xpath('.//span[@class="units"]/text()').get().strip()
            all_params = key + ': ' + value
            get_params.append(all_params.replace('[', '').replace(']', ''))

        # Возвращаем информацию в виде словаря и добавляем параметры
        yield {
            'title': title,
            'photo': photo,
            'wight': wight,
            'price': all_price,
            'one_price': one_price,
            'get_params': '; '.join(get_params)
        }
