from src.lib.link_processor import LinkProcessor

class TestLinkProcessor:
    def test_process(self):
        url = 'https://www.slashdot.org/'
        link1 = '//politics.slashdot.org/sciencelol'
        link2 = 'http://www.news.com/articles/1/'
        link3 = '/politics/news/articles/1'

        assert LinkProcessor.process(link1, url) == 'https://politics.slashdot.org/sciencelol'
        assert LinkProcessor.process(link2, url) == link2
        assert LinkProcessor.process(link3, url) == 'https://www.slashdot.org/politics/news/articles/1'

    def test_trunicate_url(self):
        url1 = 'http://dev.to/'
        url2 = 'https://www.news.org'
        url3 = 'https://www.newagency.com/articles'

        assert LinkProcessor.trunicate_url(url1) == 'http://dev.to'
        assert LinkProcessor.trunicate_url(url2) == url2
        assert LinkProcessor.trunicate_url(url3) == 'https://www.newagency.com'
