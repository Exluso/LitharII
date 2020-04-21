import shutil
import os
import send2trash
import lithar_backup as lb
from wording import curtain  # remove at the end


def update_bak(source, dest):
    """Finally this function updates the file in the backup folder.
    Works in 3 phases:
    1 - detects changes
    2 - takes action to match the changes in the backup
    3 - reports the changes
    for each phase it handles in this order: adds new items, updates old items,
    removes obsolete items."""
    # todo a function that replaces outdated files with more recent ones.

    print("source:", source)
    print("dest:", dest)

    files_added = {}
    files_removed = {}
    dir_added = []
    dir_removed = []
    for active_dir, subfolders, filenames in os.walk(source):
        # mirror_dir mirrors the walking in the source tree into the dest tree
        mirror_dir = os.path.join(dest,
                                  "" if active_dir == source
                                  else os.path.relpath(active_dir, source))

        mirror_filenames = [mf for mf in os.listdir(mirror_dir)
                            if os.path.isfile(os.path.join(mirror_dir, mf))]
        mirror_subfolders = [msf for msf in os.listdir(mirror_dir)
                             if os.path.isdir(os.path.join(mirror_dir, msf))]

        # Detects new stuff
        new_files = set(filenames) - set(mirror_filenames)
        new_subfolders = set(subfolders) - set(mirror_subfolders)
        # Detects obsolete stuff (the ones that have to be removed)
        obsolete_files = set(mirror_filenames) - set(filenames)
        obsolete_subfolders = set(mirror_subfolders) - set(subfolders)

        curtain()

        # Adds new stuff
        for nsf in new_subfolders:
            new_dir = os.path.join(mirror_dir, nsf)
            shutil.copytree(os.path.join(active_dir, nsf), new_dir)
            dir_added.append(nsf)

        local_new_files = []
        for nf in new_files:
            shutil.copy2(os.path.join(active_dir, nf), mirror_dir)
            local_new_files.append(nf)
            files_added.update({mirror_dir: local_new_files})

        # Removes obsolete stuff
        for osf in obsolete_subfolders:
            to_the_bin = shutil.move(os.path.join(mirror_dir, osf),
                                     os.path.join(mirror_dir, osf + "_bak"))
            send2trash.send2trash(to_the_bin)
            dir_removed.append(to_the_bin[:-4])  # removes "_bak" from the print

        local_removed_files = []
        for outdated_file in obsolete_files:
            to_the_bin = shutil.move(os.path.join(mirror_dir, outdated_file),
                                     os.path.join(mirror_dir, outdated_file
                                                  + "_bak"))
            send2trash.send2trash(to_the_bin)
            local_removed_files.append(outdated_file)
            files_removed.update({mirror_dir: local_removed_files})

        #debugs
        # print("filenames:", filenames)
        # print("mirror files:", mirror_filenames)
        # print("new files:", new_files)

    # Reports changes
    if dir_added:
        print("The following subfolders have been added with their content:")
        for f in dir_added:
            print("\t", f)

    for k in files_added:
        print("new addition in " + k + ":")
        for file in files_added[k]:
            print("\t" + file)

    if dir_removed:
        print("The following directories, including their contents,"
              " have been removed:")
        for folder in dir_removed:
            print("\t", folder)

    for k in files_removed:
        print("File removed from " + k + ":")
        for file in files_removed[k]:
            print("\t", file)


if __name__ == "__main__":
    t_source = os.path.join("C:\\", "Users", "pgmic", "Desktop", "Start_bak")
    t_dest = os.path.join("C:\\", "Users", "pgmic", "Desktop", "CT_test")
    update_bak(t_source, t_dest)

# TODO handling the updates in each phase
# todo TESTING TESTING MAKE TEST CASES!
# TODO replace the hardcoded text in Report changes
# TODO rewrite the code to fit in lithar, using the lithar_backup (bak) objects
