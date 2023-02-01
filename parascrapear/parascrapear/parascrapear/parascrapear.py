import scrapy
import gspread

frases_lista = []
gc = gspread.service_account(filename='/C:/Users/Pablo Malo/software-development-projects/web-scraping-project-4/scraping-link-376521-f236a3695e51.json')

# Abrir por titulo
sh = gc.open("Frases")

# Seleccionar primera hoja
worksheet = sh.get_worksheet(0)

class ParascrapearSpider(scrapy.Spider):
    name = "parascrapear"
    allowed_domains = ["parascrapear.com"]
    start_urls = ["https://parascrapear.com/"]

    def parse(self, response):
        print("Parseando " + response.url)

        next_urls = response.css("a::attr(href)").getall()
        for next_url in next_urls:
            if next_url is not None:
                yield scrapy.Request(response.urljoin(next_url))

        frases = response.css("q::text").getall()
        for frase in frases:
            if frase is not frases_lista:
                frases_lista.append(frase)
                row_index = len(worksheet.col_values(1)) + 1
                worksheet.update("A" + str(row_index), frase)