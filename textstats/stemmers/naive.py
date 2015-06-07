class NaiveStemmer:
    def __init__(self, strip=3, offset=3):
        """
        Set stemming preferences.

        Parameters 
        ----------
        tokens: list
            A list of candidate tokens for stemming. The naive stemmer
            provides no validation, so users must ensure that tokens are
            as desired before passing them to the stemmer.

        offset: int (optional)
            A number of characters beyond 'strip' to require before a token
            can be stemmed. Ex: offset=3 and strip=3 means that a token must
            be 6 chars or longer before stemming is applied.

        strip (int, optional): number of characters to strip to create
            word stems.
        """
        self.offset = offset
        self.strip = strip

    def stem(self, tokens):
        """ 
        Stem a list of tokens of sufficient length by removing the last
        N characters.
        """
        return [token[:-self.strip] if len(token) >= self.strip + self.offset else token for token in tokens]