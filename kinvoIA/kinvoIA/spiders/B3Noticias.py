# -*- coding: utf-8 -*-
import scrapy
from kinvoIA.items import KinvoiaItem


class B3noticiasSpider(scrapy.Spider):
    name = 'B3Noticias' 
    allowed_domains = ['b3.com.br/pt_br/noticias/']
    start_urls = ['http://b3.com.br/pt_br/noticias//']

    def parse(self, response):
     
        titulo = response.xpath('//h4/text()').extract()
        noticiadata = response.xpath('//p/text()').extract()

        noticia = KinvoiaItem(titulo = titulo, noticiadata = noticiadata)
        yield noticia

  #      for new in response.css('div.card.clickable'):       
   #         titulo = new.xpath('//h4/text()').extract_first()
  #          noticiadata = new.xpath('//p/text()').extract_first()
  #          yield ({'titulo': titulo, 'noticia&data': noticiadata})