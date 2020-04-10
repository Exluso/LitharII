""" This module contains the BakData class for LitharII, a collection of
metadata of the backups."""
import datetime


class BakData:
    """Holds the metadata used by Lithar II to work with backups."""

    def __init__(self, lithar, name, notes, source, dest):
        """IN: the lithar instance they belong to, in order to access its
        methods and attributes."""
        self.lithar = lithar
        # data for Lithar.opt_dicts
        self.name = name
        self.notes = notes
        self.mod_date = datetime.datetime.now()  # date of creation/last update
        # full path of the original folder and the destination
        self.source = source
        self.dest = dest

    def pretty_date(self):
        """ formats the self.mod_date."""
        pretty_date = self.mod_date.strftime("%d %b %Y")
        return pretty_date

    def gen_description(self):
        """returns a 'description' to be used by lithar.opt_dict."""
        # todo test that it works when accessing lithar settings
        desc = self.name.ljust(self.lithar.settings.space_name) \
               + self.pretty_date().ljust(self.lithar.settings.space_note) \
               + self.notes
        return desc

    #  path getters
    def get_source_path(self):
        return self.source

    def get_dest_path(self):
        return self.dest


if __name__ == "__main__":
    bac = BakData("test", "testName", "test_desc", "testSource", "testDest")
    print(bac.mod_date)
    print(bac.pretty_date())
    print(bac.gen_description())
