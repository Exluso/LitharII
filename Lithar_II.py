""" A better Lithar.
Because re-writing is better than refactoring."""
import time
import sys
import os
import shelve
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
        self.load_bak_list()
        # a opt_dict list that contains the backup obj.
        self._init_opt_bak_list()

    def _init_opt_dict_stuff(self):
        """ a helper method that initialize all the attributes related
        to the opt_dictionaries."""
        od.init_opt_dictionaries(self)
        od.init_opt_lists(self)

    def _init_opt_bak_list(self):
        """initialize the opt_dict list used to select a saved backup."""
        self.opt_bak_list = []
        for bak in self.bak_list:
            self.opt_bak_list.append(
                od.gen_opt_dict(od.gen_bak_description(self, bak), curtain)
            )

    def main(self):
        """The main function that puts and keeps things in motion."""
        curtain()
        print(self.texts["welcome"])
        while True:
            self.option_frame(self.main_options)

    def option_frame(self, opt_list, header=""):
        """prints a numbered list from which is possible to select options.
        IN: opt_list a list of dictionary representing the options."""
        print()
        print(self.texts["choose_option"])
        print()
        print(header)
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

    def option_frame_baklist(self):
        """ wrapper function for displaying the bak_list option frame.
        activates only if there are already bak in the bak_list."""
        if len(self.bak_list) > 0:
            headers = (self.texts["opt_fr_baklist_index"].ljust(3) + "  - "
                  + self.texts["opt_fr_baklist_name"].ljust(\
                self.settings.space_name)
                  + self.texts["opt_fr_baklist_date"].ljust(\
                self.settings.space_date)
                  + self.texts["opt_fr_baklist_notes"])

            self.option_frame(self.opt_bak_list, headers)
        elif len(self.bak_list) <= 0:
            print("\n" + self.texts["err_no_save"])

    def quit_lithar(self):
        """ quit the program."""
        print()
        answer = input(self.texts["quit_confirm"])
        if answer in self.settings.positive_answer:
            print(self.texts["byez"])
            time.sleep(2)
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
        # todo check if the name attribute is already used by another
        #  bak object in opt_bak_list
        notes = input(self.texts["new_bak_input_note"])
        source = input(self.texts["new_bak_input_source"])
        dest = input(self.texts["new_bak_input_dest"])

        self.bak_list.append(bak.BakData(name, notes, source, dest))
        self.save_bak_list()
        self._init_opt_bak_list()
        # todo a function that actually creates the backup folder :D
        print()
        print(self.texts["new_bak_created"] % self.bak_list[-1].name)

    def save_bak_list(self):
        """ creates or upaates a json file containing the bak_list."""
        with shelve.open(self.settings.savefile) as savefile:
            savefile["bak_list"] = self.bak_list

    def load_bak_list(self):
        """ load the bak_list with previously made bak_data. If the savefile
        is not present it will inform the user."""
        if self._has_savedata():
            with shelve.open(self.settings.savefile) as savefile:
                self.bak_list = savefile["bak_list"]
        elif not self._has_savedata():
            print(self.texts["err_no_save"])
            self.bak_list = []

    def _has_savedata(self):
        """check is the shelve files are already present.
        This works only in Windows."""
        #  todo write it so it works also on MacOs using only .dir
        has_data = False
        if (os.path.isfile(self.settings.savefile + ".bak") and
                os.path.isfile(self.settings.savefile + ".dat") and
                os.path.isfile(self.settings.savefile + ".dir")):
            has_data = True
        return has_data

    def test(self):
        print(self.settings.language)
        print("bak_list: ", lithar.bak_list)
        lithar.load_bak_list()


if __name__ == "__main__":
    lithar = Lithar()
    lithar.main()
    # lithar.test()
else:
    lithar = Lithar()
    lithar.test()
