class Settings():
    """ Holds several settinggs used by Lithar II"""
    def __init__(self, lithar):
        """ IN: lithar: the main class of the program to access her data."""
        self.language = "ENG" # default language of the script
        # default user input for yes/no question
        # todo consider making them dependant from the txt file (low prio)
        self.positive_answer = ["y", "yes", "s", "sì"]
        self.negative_answer = ["n", "no"]
        # spacing used in the layout of the index of the current backup
        self.space_name = 20
        self.space_date = 23
        self.space_note = 20
        # savefile name
        self.savefile = "lithar_savefile"
