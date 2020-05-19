class LinkProcessor:
    @classmethod
    def process(cls, link, url):
        if link[0:2] == '//':
            return link.replace('//', 'https://')
        elif link[0:4] == 'http':
            return link    

        return f"{url}{link}"
