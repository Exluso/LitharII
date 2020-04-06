""" A better Lithar.
Because re-writing is better than refactoring."""

from settings import Settings
from texts import create_texts, separe
class Lithar():
    """The main class that keeps things running"""

    def __init__(self):
        self.settings = Settings()
        self.texts = create_texts(self.settings.language)

    def main(self):
        """The main function that puts and keeps things in motion."""
        #Todo check for a savefile, prints options.

    def test(self):
        print(self.settings.language)
        print(self.texts["welcome"])



lithar = Lithar()
lithar.test()