class LinkProcessor:
    @classmethod
    def process(cls, link, url):
        if link[0:2] == '//':
            return link.replace('//', 'https://')

        return f"{url}{link}"
