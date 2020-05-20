class LinkProcessor:
    @classmethod
    def process(cls, link, url):
        if link[0:2] == '//':
            return link.replace('//', 'https://')
        elif link[0:4] == 'http':
            return link

        return f"{cls.trunicate_url(url)}{link}"

    @classmethod
    def trunicate_url(cls, url):
        endpos = url[8:].find('/')
        if endpos > -1:
            return url[0:(endpos + 8)]
        elif endpos == -1:
            return url[0:8] + (url[8:].replace('/', ''))

        return url
