""" A better Lithar.
Because re-writing is better than refactoring.

Keep in mind the following status for Lithar II:
'main'  = the initial and default status, leads to the 'main_options' opt_list
'index' = the status is activated when the bak index is displayed, this allows
to pass an argument when using the opt_list[choice]["action"]() """
import time
import sys
import os
import shutil
import shelve
import opt_dictionaries as od
import lithar_backup as lb
import update_bak_func as update_module
from settings import Settings
from wording import create_texts, curtain


class Lithar:
    """The main class that keeps things running"""

    def __init__(self):
        self.status = ""
        self.settings = Settings(self)
        self.texts = create_texts(self.settings.language)
        self._init_opt_dict_stuff()
        self.load_bak_list()
        # a opt_dict list that contains the backup obj.
        self._init_opt_bak_list()
        self.target = None

    def _init_opt_dict_stuff(self):
        """ a helper method that initialize all the attributes related
        to the opt_dictionaries."""
        od.init_opt_dictionaries(self)  # a list of all
        od.init_opt_lists(self)

    def _init_opt_bak_list(self):
        """initialize the opt_dict list used to select a saved backup."""
        self.opt_bak_list = []
        for bak in self.bak_list:
            self.opt_bak_list.append(
                od.gen_opt_dict(od.gen_bak_description(self, bak),
                                self.option_frame_access_bak)
            )
        self.opt_bak_list.append(self.opt_go_back)

    def main(self):
        """The main function that puts and keeps things in motion."""
        curtain()
        print(self.texts["welcome"])
        while True:
            self.status = "main"
            self.target = None
            self._init_opt_bak_list()
            self.option_frame(self.main_options)

    def option_frame(self, opt_list, header=""):
        """prints a numbered list from which is possible to select options.
        IN: opt_list a list of dictionary representing the options."""
        curtain()
        print()
        print(self.texts["choose_option"])
        print()
        if header:
            print(header)
        for opt in opt_list:
            print(f"{opt_list.index(opt)}".ljust(3),
                  f" - {opt['description']}")

        try:
            choice = int(input(self.texts["enter_num"]))

            # calls the "action" value (i.e. a function) of the
            # dictionary (option) at the choice index of the opt_list
            # if in 'index' status also provides an argument
            if self.status == "index":
                opt_list[choice]["action"](choice)
            else:
                opt_list[choice]["action"]()

        except (ValueError, IndexError):
            print(self.texts["error"] + self.texts["err_option_input"])

    def option_frame_baklist(self):
        """ wrapper function for displaying the bak_list option frame.
        activates only if there are already bak in the bak_list."""
        self.status = 'index'
        if len(self.bak_list) > 0:
            headers = (self.texts["opt_fr_baklist_index"].ljust(3) + " - "
                       + self.texts["opt_fr_baklist_name"].ljust(
                        self.settings.space_name)
                       + self.texts["opt_fr_baklist_date"].ljust(
                        self.settings.space_date)
                       + self.texts["opt_fr_baklist_notes"])

            self.option_frame(self.opt_bak_list, headers)
        elif len(self.bak_list) <= 0:
            print("\n" + self.texts["err_no_save"])

    def option_frame_access_bak(self, bak_index):
        """The option frame that prompts actions related to a specific bak."""
        self.target = self.bak_list[bak_index]
        self.status = 'main'
        header = self.texts["access_bak_header"] % self.target.name
        self.option_frame(self.opt_bak_op_list, header)

    def go_back(self, arg=None):
        """Fake function used to go back in the menu."""
        pass

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
        name_flag = True
        while name_flag:
            new_name = input(self.texts["new_bak_input_name"])
            name_flag = self._name_check(new_name)
        notes = input(self.texts["new_bak_input_note"])

        path_flag = True
        while path_flag:
            path_exist = False
            while not path_exist:
                source = input(self.texts["new_bak_input_source"])
                path_exist = self._path_check(source)
            path_exist = False
            while not path_exist:
                dest = input(self.texts["new_bak_input_dest"])
                path_exist = self._path_check(dest)

            if source in dest:
                print(self.texts["err_path_check"])
            elif source not in dest:
                path_flag = False

        self.bak_list.append(lb.BakData(new_name, notes, source, dest))
        self.save_bak_list()
        self._init_opt_bak_list()
        try:
            # The line that actually copies folders and files!
            shutil.copytree("\\\\?\\" + source,
                            os.path.join("\\\\?\\" + dest, os.path.basename(source)
                                         + "_bak"))
            self.bak_list[-1].dest = os.path.join(dest,
                                                  os.path.basename(source + "_bak"))
            self.save_bak_list()
            print()
            print(self.texts["new_bak_created"] % self.bak_list[-1].name)
        except FileExistsError:
            print(self.texts["err_bak_already_exist"])
            time.sleep(5)

    def _name_check(self, name):
        """ checks if the new bak is going to have a name already used for
        a prvious bak. This should help avoid confusion."""
        for bak in self.bak_list:
            if name == bak.name:
                print(self.texts["err_name_check"])
                return True
            else:
                return False

    def _path_check(self, path):
        """Checks if a path really exists."""
        if path[-1] == ":":
            print(self.texts["err_path_is_hd"] % os.sep)
            return False
        if not os.path.exists(path):
            print(self.texts["err_no_path"])
            return False
        else:
            return True

    def bak_details(self):
        """ shows the details of the selected backup. Details are such:
        sourcepath, destination path, notes, last update time."""
        curtain()
        print(self.texts["bak_det_title"])
        print(f'{self.texts["bak_det_name"]}'.ljust(self.settings.space_note) +
              f'{self.target.name}')
        print(f'{self.texts["bak_det_last_update"]}'.ljust(
            self.settings.space_note) + f'{self.target.mod_date}')
        print(f'{self.texts["bak_det_dest"]}'.ljust(self.settings.space_note) +
              f'{self.target.dest}')
        print(f'{self.texts["bak_det_source"]}'.ljust(
            self.settings.space_note) + f'{self.target.source}')

    def update_bak(self):
        update_module.update_bak(self, self.target)

    def del_bak(self):
        """ Removes a bak from the bak_list and hence from the savefile.
        NOTE: this does not deletes the actual backup folder, only the index in
        Lithar."""
        curtain()
        print(self.texts["del_bak_note"] + "\n")
        confirm = input((self.texts["del_bak_confirm"] % self.target.name))
        if confirm in self.settings.positive_answer:
            self.bak_list.remove(self.target)
            self.save_bak_list()
            print(self.texts["del_bak_done"] % self.target.name)
        elif confirm in self.settings.negative_answer:
            pass
        else:
            print(self.texts["noidea"])

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
