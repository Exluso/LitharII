""" A better Lithar.
Because re-writing is better than refactoring."""
import time
import sys
import opt_dictionaries as od
import lithar_backup as bak
from settings import Settings
from wording import create_texts, curtain


class Lithar:
    """The main class that keeps things running"""

    def __init__(self):
        self.settings = Settings(self)
        self.texts = create_texts(self.settings.language)
        self._init_opt_dict_stuff()
        self.bak_list = []  # contains the BakData objects available atm

    def _init_opt_dict_stuff(self):
        """ a helper method that initialize all the attributes related
        to the opt_dictionaries."""
        od.init_opt_dictionaries(self)
        od.init_opt_lists(self)

    def main(self):
        """The main function that puts and keeps things in motion."""
        curtain()
        print(self.texts["welcome"])
        while True:
            self.option_frame(self.main_options)

        # Todo check for a savefile, prints options.

    def option_frame(self, opt_list):
        """prints a numbered list from which is possible to select options.
        IN: opt_list a list of dictionary representing the options."""
        print()
        print(self.texts["choose_option"])
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
        print()
        answer = input(self.texts["quit_confirm"])
        if answer in self.settings.positive_answer:
            print(self.texts["byez"])
            time.sleep(5)
            sys.exit()
        elif answer in self.settings.negative_answer:
            pass
        else:
            print(self.texts["no_idea"])

    def set_language(self):
        """ Asks for the user input about the language and formats it for
        _change_language."""
        print()
        user_lang = input(self.texts["ins_lang"])
        lang = user_lang[:3].upper()
        self._change_language(lang)

    def _change_language(self, lang):
        """ change the language settings
        IN: lang a 3 capital letters string, the initials
        of the new language."""
        try:
            self.settings.language = lang
            self.texts = create_texts(self.settings.language)
            self._init_opt_dict_stuff()

        except KeyError:
            print(self.texts["error"] + self.texts["err_lang_input"])

    def new_bak(self):
        """creates a new backup, adds it to the bak_list."""
        name = input(self.texts["new_bak_input_name"])
        notes = input(self.texts["new_bak_input_note"])
        source = input(self.texts["new_bak_input_source"])
        dest = input(self.texts["new_bak_input_dest"])

        self.bak_list.append(bak.BakData(self, name, notes, source, dest))

        print(self.bak_list[0].name)


    def test(self):
        print(self.settings.language)
        print(self.texts["welcome"])


if __name__ == "__main__":
    lithar = Lithar()
    lithar.main()
    # lithar.test()
else:
    lithar = Lithar()
    lithar.test()
