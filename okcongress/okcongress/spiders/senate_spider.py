import scrapy
import html2text
import re

class SenateSpider(scrapy.Spider):
    name = "senate_members"
    start_urls = [ 'http://www.oksenate.gov/Senators/Default.aspx?selectedtab=0' ]
    
    def parse(self, response):
        hrefs = response.xpath('//table[@summary="This table lists the Senators alphabetically.  Each senator\'s name is linked to his or her respective contact page."]/tr/td/span/span/a/@href').extract()[:48]
        
        for href in hrefs:
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_senator)
        
    def parse_senator(self, response):
        yield scrapy.Request(
            response.urljoin(response.xpath('//iframe/@src').extract_first()),
            callback=self.parse_senator_iframe)
    
    
    def parse_senator_iframe(self, response):
        htmlstrip = html2text.HTML2Text()
        htmlstrip.ignore_links = True
        #sen_re = re.compile(r'Senator (.*) - District (\d+)')
        sen_re = re.compile(r'(?:Senator )?\b(.*)\s*-\s*District\s*(\d+)')
        phone_re = re.compile(r'\(?(405|918)\)?.?(\d{3}).?(\d{4})')
        room_re = re.compile(r'(Rm\.|Room)\s*([0-9a-zA-Z]+)')
        
        markdown_page = htmlstrip.handle(response.body_as_unicode()).replace('\\', '').replace('*', '')
        name, dist = sen_re.findall(markdown_page)[0]
        
        district = int(dist)
        fname = name.split()[0]
        lname = name.split()[-1]
        
        phone = '-'.join(phone_re.findall(markdown_page)[0])
          
        cmtes = response.xpath('//html/body/table/tr/td/table/tr[4]/td/ul[1]/li').extract()
        cmtes = map(htmlstrip.handle, cmtes)
        cmtes = map(lambda a: a.split(' ', 1)[1].replace('*', '').strip(), cmtes)
        
        # Remove Chair, etc:
        cmtes = map(lambda a: a.split('\\-')[0].strip(), cmtes)
        
        room = room_re.findall(markdown_page)[0][1]
                
        party_letter = response.xpath('//html/body/table/tr/td/table/tr/td').re(r'Republican|Democrat|Libertarian')[0][0]
                
        return dict(
            fname=fname,
            lname=lname,
            name=name,
            district=district,
            party=party_letter,
            committees=cmtes,
            office=room,
            phone=phone
        )