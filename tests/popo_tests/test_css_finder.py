from src.lib.css_finder import CssFinder

class TestCssFinder:
    def test_find_tag(self):
        url1 = 'https://asiatimes.com/world/usa/'
        url2 = 'https://slashdot.org/'

        assert CssFinder.find_tag(url2) == 'story-title'
        assert CssFinder.find_tag(url1) == 'entry-title'
