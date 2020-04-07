""" A better Lithar.
Because re-writing is better than refactoring."""

from settings import Settings
from wording import create_texts, separe


class Lithar:
    """The main class that keeps things running"""

    def __init__(self):
        self.settings = Settings(self)
        self.texts = create_texts(self.settings.language)
        # todo the text in the options does not change
        #  when changing the language. Fix it.
        self.opt_chanlan = {"description": self.texts["change_lang"],
                            "action": self.set_language}
        self.main_options = [self.opt_chanlan]

    def main(self):
        """The main function that puts and keeps things in motion."""
        separe()
        print(self.texts["welcome"])
        print()
        self.option_frame(self.main_options)

        # Todo check for a savefile, prints options.

    def option_frame(self, opt_list):
        """prints a numbered list from which is possible to select options.
        IN: opt_list a list of dictionary representing the options."""
        print(self.texts["choose_option"])
        while True:
            for opt in opt_list:
                print(f"{opt_list.index(opt)}".ljust(3),
                      f" - {opt['description']}")

            try:
                choice = int(input(self.texts["enter_num"]))

                # calls the "action" value (i.e. a function) of the
                # dictionary (option) at the choice index of the opt_list
                opt_list[choice]["action"]()

            except (ValueError, IndexError):
                print(self.texts["error"] + self.texts["err_option_input"])

    def quit_lithar(self):
        """ quit the program."""
        # todo this function
        pass
        
    def set_language(self):
        """ Asks for the user input about the language and formats it for
        _change_language."""
        print()
        user_lang = input(self.texts["ins_lang"])
        lang = user_lang[:3].upper()

        self._change_language(lang)
        print(self.texts["welcome"])

    def _change_language(self, lang):
        """ change the language settings
        IN: lang a 3 capital letters string, the initials
        of the new language."""
        try:
            self.settings.language = lang
            self.texts = create_texts(self.settings.language)
        except KeyError:
            print(self.texts["error"] + self.texts["err_lang_input"])


    def test(self):
        print(self.settings.language)
        print(self.texts["welcome"])
        self._change_language("tre")


if __name__ == "__main__":
    lithar = Lithar()
    lithar.main()
    # lithar.test()
