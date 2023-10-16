class SmbQuote:

    def __init__(self):
        self._id = None
        self._tags = []
        self._author = None
        self._quote = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, str):
            self._id = value
        else:
            raise ValueError('ID must be a string!')

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if isinstance(value, list):
            if all(isinstance(tag, str) for tag in value):
                self._tags = value
            else:
                raise ValueError('All tags must be strings')

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, str):
            self._author = value
        else:
            raise ValueError('Author must be a string')

    @property
    def quote(self):
        return self._quote

    @quote.setter
    def quote(self, value):
        if isinstance(value, str):
            self._quote = value
        else:
            raise ValueError('Quote must be a string.')

    def init_rows(self, fromDict: {}):
        self._id = fromDict['id']
        self._author = fromDict['author']
        self._quote = fromDict['quote']
        self._tags = fromDict['tags']
