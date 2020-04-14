"""This module contains the opt_dictionaries used in Lithar II.
a opt_dictionary is a dictionary used by Lithar to present options and choices
to the user.
Naming: opt_ + name of the function
Keys:
    'description': a description for the final user.
    'action': the function that will perform the action chosen by the user
opt_dicts are also used to present the already available lithar_backups to
the user, they use the same format but are referred as 'opt_bak'
Naming: opt_bak + ???
'description': comes from the lithar_backup.gen_description
'action': lithar.option_frame_access_bak() function"""


def gen_opt_dict(desc, func):
    """ generates a single opt_dict """
    opt_dict = {"description": desc,
                "action": func
                }
    return opt_dict


def gen_bak_description(lithar, bak):
    """generate a description of the lithar_backup object (bak)"""
    # todo a way to handle long names that mess with the layout
    desc = (bak.name.ljust(lithar.settings.space_name)
            + bak.pretty_date().ljust(lithar.settings.space_date)
            + bak.notes)
    return desc


def init_opt_dictionaries(lithar):
    """ initialize the opt_dictionaries for Lithar."""
    lithar.opt_access_bak = gen_opt_dict(lithar.texts["access_bak_desc"],
                                         lithar.option_frame_baklist)
    lithar.opt_chanlan = gen_opt_dict(lithar.texts["change_lang_desc"],
                                      lithar.set_language)
    lithar.opt_newbak = gen_opt_dict(lithar.texts["new_bak_desc"],
                                     lithar.new_bak)
    lithar.opt_quit = gen_opt_dict(lithar.texts["quit_desc"],
                                   lithar.quit_lithar)


def init_opt_lists(lithar):
    """ initialize the lists of opt_dict to be used in lithar.option_frame()"""
    lithar.main_options = [lithar.opt_chanlan,
                           lithar.opt_quit,
                           lithar.opt_newbak,
                           lithar.opt_access_bak]

    # todo access_bak_options
