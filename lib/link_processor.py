class LinkProcessor:
    @classmethod
    def process(cls, link, url):
        if link[0:1] == '//':
            return link.replace('//', 'https://')

        return f"{url}{link}"    
