""" This module contains the BakData class for LitharII, a collection of
metadata of the backups."""
import datetime


class BakData:
    """Holds the metadata used by Lithar II to work with backups."""

    def __init__(self, name, notes, source, dest):
        """IN: the lithar instance they belong to, in order to access its
        methods and attributes."""
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

    #  path getters
    def get_source_path(self):
        return self.source

    def get_dest_path(self):
        return self.dest


if __name__ == "__main__":
    bac = BakData("testName", "test_desc", "testSource", "testDest")
    print(bac.mod_date)
    print(bac.pretty_date())
