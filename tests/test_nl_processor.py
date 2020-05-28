from src.lib.nl_processor import NLProcessor

class TestNLProcessor:
    def setup(self):
        self.nlp = NLProcessor()

    def test_is_sentence(self):
        phrase1 = 'Hello'
        phrase2 = 'Anti-Porn Filters Stop Dominic Cummings Trending On Twitter'
        phrase3 = 'Japan Enacts High-Tech Super City Bill Where AI, Big Data and Other Technologies Are Utilized To Resolve Social Problems'

        assert not self.nlp.is_sentence(phrase1)
        assert self.nlp.is_sentence(phrase2)
        assert not self.nlp.is_sentence(phrase3, 'cssfind')
        assert self.nlp.is_sentence(phrase3)
