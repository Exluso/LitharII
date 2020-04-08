class Settings():
    """ Holds several settinggs used by Lithar II"""
    def __init__(self, lithar):
        """ IN: lithar: the main class of the program to access her data."""
        self.language = "ENG"
        self.positive_answer = ["y", "yes", "s", "sì"]
        self.negative_answer = ["n", "no"]
