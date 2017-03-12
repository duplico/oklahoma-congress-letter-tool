import scrapy


class HouseSpider(scrapy.Spider):
    name = "house_members"
    start_urls = [ ('http://www.okhouse.gov/Members/District.aspx?District=%d' % dist) for dist in range(1,102) ]

    def parse(self, response):
        name = ' '.join(response.xpath('//span[@id="ctl00_ContentPlaceHolder1_lblName"]/text()').extract_first().split()[1:])
        district = int(response.url.split('=')[-1])
        party = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_lblParty"]/text()').extract_first()
        party_letter = party[0]
        
        committees = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_lblCommittees"]/a/text()').extract()
        office = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_lblCapitolRoom"]/text()').extract_first()
        phone = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_lblPhone"]/text()').extract_first()
        
        return dict(
            fname=name.split()[0],
            lname = name.split()[-1],
            district=district,
            party=party_letter,
            committees=committees,
            office=office,
            phone=phone
        )