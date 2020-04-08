"""This module contains the opt_dictionaries used in Litar II.
a opt_dictionary is a dictionary used by Lithar to present options and choices
to the user.
Naming: opt_ + name of the function
Keys:
    'description': a description for the final user.
    'action': the function that will perform the action chosen by the user"""


def gen_opt_dict(desc, func):
    """ generates the opt_dict """
    opt_dict = {"description": desc,
                "action": func
                }
    return opt_dict


def init_opt_dictionaries(lithar):
    """ initialize the opt_dictionaries for Lithar."""
    lithar.opt_chanlan = gen_opt_dict(lithar.texts["change_lang_desc"],
                                      lithar.set_language)
    lithar.opt_quit = gen_opt_dict(lithar.texts["quit_desc"],
                                   lithar.quit_lithar)


def init_opt_lists(lithar):
    """ initialize the lists of opt_dict to be used in lithar.option_frame()"""
    lithar.main_options = [lithar.opt_chanlan, lithar.opt_quit]
