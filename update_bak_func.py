import shutil
import os
import send2trash


# TODO Updates the upper folder instead of the proper one!!!
# TODO Don't tst on your desktop you idiot :D

def update_bak(lithar, bak):
    """Finally this function updates the file in the backup folder.
    Works in 3 phases:
    1 - detects changes
    2 - takes action to match the changes in the backup
    3 - reports the changes
    for each phase it handles in this order: adds new items, updates old items,
    removes obsolete items."""

    def add_folder(new_folder):
        """Adds a new folder in the backup."""
        new_dir = os.path.join(mirror_dir, new_folder)
        shutil.copytree(os.path.join(active_dir, new_folder), new_dir)
        dir_added.append(new_dir)

    def add_file(new_file):
        """ add a new file to the bak."""
        shutil.copy2(os.path.join(active_dir, new_file), mirror_dir)
        local_new_files.append(new_file)
        files_added.update({mirror_dir: local_new_files})

    def isOutdated(filename):
        """Returns True if file in source is more recent than file in bak."""
        file_source_mtime = os.path.getmtime(os.path.join(active_dir, filename))
        file_bak_mtime = os.path.getmtime(os.path.join(mirror_dir, filename))
        if file_source_mtime > file_bak_mtime:
            return True

    def update_file(filename):
        """replaces an outdated file with its most recent version."""
        shutil.copy2(os.path.join(active_dir, filename),
                     os.path.join(mirror_dir))
        local_updated_files.append(filename)
        files_updated.update({mirror_dir: local_updated_files})

    def rem_folder(obsolete_folder):
        """ Removes a folder from the bak, that is not in the source anymore."""
        to_the_bin = shutil.move(os.path.join(mirror_dir, obsolete_folder),
                                 os.path.join(mirror_dir, obsolete_folder
                                              + "_bak"))
        send2trash.send2trash(to_the_bin)
        dir_removed.append(to_the_bin[:-4])  # removes "_bak" from the print

    def rem_file(obsolete_file):
        """Removes a file from the bak that is not in the source anymore"""
        to_the_bin = shutil.move(os.path.join(mirror_dir, obsolete_file),
                                 os.path.join(mirror_dir, obsolete_file
                                              + "_bak"))
        send2trash.send2trash(to_the_bin)
        local_removed_files.append(obsolete_file)
        files_removed.update({mirror_dir: local_removed_files})

    def report_changes(changes):
        """ Prints out the changes, using a different style if the changes are
        about files (INPUT:changes as dict) or about folders (INPUT as list)"""
        if type(changes) == list:
            if len(changes) >= 2:
                print(changes[0])
                for subfolder in changes[1:]:
                    print("\t", subfolder)
        elif type(changes) == dict:
            if len(changes) >= 2:
                for k in changes:
                    if k != "text":
                        print(changes["text"] % k)
                    for file_changed in changes[k]:
                        if k != "text":
                            print("\t" + file_changed)

    source = bak.source
    dest = bak.dest
    #print("source:", source)
    #print("dest:", dest)

    files_added = {"text": lithar.texts["update_bak_added_file"]}
    files_updated = {"text": lithar.texts["update_bak_updated_file"]}
    files_removed = {"text": lithar.texts["update_bak_remd_file"]}
    dir_added = [lithar.texts["update_bak_added_dir"]]
    dir_removed = [lithar.texts["update_bak_remd_dir"]]
    for active_dir, subfolders, filenames in os.walk(source):
        # mirror_dir mirrors the walking in the source tree into the dest tree
        mirror_dir = os.path.join(dest,
                                  "" if active_dir == source
                                  else os.path.relpath(active_dir, source))
        #print("active:", active_dir)
        #print("mirror:", mirror_dir)
        mirror_filenames = [mf for mf in os.listdir(mirror_dir)
                            if os.path.isfile(os.path.join(mirror_dir, mf))]
        mirror_subfolders = [msf for msf in os.listdir(mirror_dir)
                             if os.path.isdir(os.path.join(mirror_dir, msf))]

        # Detects new stuff
        new_files = set(filenames) - set(mirror_filenames)
        new_subfolders = set(subfolders) - set(mirror_subfolders)
        # Detects files that are already in the backup
        previous_files = set(filenames) & set(mirror_filenames)
        # Detects obsolete stuff (the ones that have to be removed)
        obsolete_files = set(mirror_filenames) - set(filenames)
        obsolete_subfolders = set(mirror_subfolders) - set(subfolders)

        # Adds new subfolders
        for new_sub_folder in new_subfolders:
            add_folder(new_sub_folder)
        # Adds new files
        local_new_files = []
        for file in new_files:
            add_file(file)
        # Updates outdated files
        local_updated_files = []
        for file in previous_files:
            if isOutdated(file):
                update_file(file)
        # Removes obsolete folders
        for obs_folder in obsolete_subfolders:
            rem_folder(obs_folder)
        # Removes obsolete files
        local_removed_files = []
        for obs_file in obsolete_files:
            rem_file(obs_file)

    # Reports changes
    list_of_changes = [dir_added, files_added, files_updated,
                       dir_removed, files_removed]
    report = False
    for item in list_of_changes:
        if len(item) > 1:
            report = True
            report_changes(item)
    if not report:
        print(lithar.texts["update_bak_no_update"])


if __name__ == "__main__":
    t_source = os.path.join("C:\\", "Users", "pgmic", "Desktop", "Start_bak")
    t_dest = os.path.join("C:\\", "Users", "pgmic", "Desktop", "CT_test")
    print("Running on your own?")
