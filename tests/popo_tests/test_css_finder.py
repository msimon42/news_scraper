from src.lib.css_finder import CssFinder

class TestCssFinder:
    def setup(self):
        self.css_finder = CssFinder()

    def test_find_tag(self):
        url1 = 'https://asiatimes.com/world/usa/'
        url2 = 'https://slashdot.org/'

        assert self.css_finder.find_tag(url2) == 'story-title'
        assert self.css_finder.find_tag(url1) == 'entry-title'
