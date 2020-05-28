from src.lib.link_processor import LinkProcessor

class TestLinkProcessor:
    def test_process(self):
        url = 'https://www.slashdot.org/'
        link1 = '//politics.slashdot.org/sciencelol'
        link2 = 'http://www.news.com/articles/1/'
        link3 = '/politics/news/articles/1'

        
