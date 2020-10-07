from src.lib.css_finder import CssFinder

class TestCssFinder:
    def setup(self):
        self.css_finder = CssFinder()

    def test_find_tag(self):
        url1 = 'https://www.reuters.com/news/technology'
        url2 = 'https://www.slashdot.org/'

        assert self.css_finder.find_tag(url2) == 'story-title'
        assert self.css_finder.find_tag(url1) == 'story-content'
