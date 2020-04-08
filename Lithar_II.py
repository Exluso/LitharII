""" A better Lithar.
Because re-writing is better than refactoring."""
import time
import sys
import opt_dictionaries as od
from settings import Settings
from wording import create_texts, curtain


class Lithar:
    """The main class that keeps things running"""

    def __init__(self):
        self.settings = Settings(self)
        self.texts = create_texts(self.settings.language)
        # todo the text in the options does not change
        #  when changing the language. Fix it.
        # The following od. functions initialize more Lithar parameters
        self.init_opt_dictionaries()
        self.init_opt_lists()

    def init_opt_dictionaries(self):
        """ initialize the opt_dictionaries for Lithar."""
        self.opt_chanlan = od.gen_opt_dict(self.texts["change_lang_desc"],
                                        self.set_language)
        self.opt_quit = od.gen_opt_dict(self.texts["quit_desc"],
                                     self.quit_lithar)

    def init_opt_lists(self):
        """ initialize the lists of opt_dict to be used in lithar.option_frame()"""
        self.main_options = [self.opt_chanlan, self.opt_quit]

    def main(self):
        """The main function that puts and keeps things in motion."""
        curtain()
        print(self.texts["welcome"])
        self.option_frame(self.main_options)

        # Todo check for a savefile, prints options.

    def option_frame(self, opt_list):
        """prints a numbered list from which is possible to select options.
        IN: opt_list a list of dictionary representing the options."""
        while True:
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
            self.init_opt_dictionaries()
            self.init_opt_lists()
            #self.opt_quit["description"] = self.texts["quit_desc"]
            self.init_opt_dictionaries()
            self.init_opt_lists()
            print(self.opt_quit)
            print(self.main_options[1])

        except KeyError:
            print(self.texts["error"] + self.texts["err_lang_input"])

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
