import shutil
import os
from wording import curtain  # remove at the end


def update_bak(source, dest):
    """Finally this function updates the file in the backup folder."""
    # todo a function that replaces outdated files with more recent ones.
    # todo a function that removes files and folder from back if the same
    #  files and folders are not in the source anymore
    # todo a function that adds files in the backup if they are in the
    #  source and not in the backup
    print("source:", source)
    print("dest:", dest)
    files_added = {}
    files_removed = {}
    dir_added = []
    dir_removed = {}
    for active_dir, subfolders, filenames in os.walk(source):
        #print("active dir:", active_dir)
        #print("\tsubfodlers:", subfolders)
        #print("\tfiles:", filenames)

        # mirror_dir mirrors the walking in the source tree into the dest tree
        mirror_dir = os.path.join(dest,
                                  "" if active_dir == source
                                  else os.path.relpath(active_dir, source))

        #print("mirror list:", os.listdir(mirror_dir))
        mirror_filenames = [mf for mf in os.listdir(mirror_dir)
                            if os.path.isfile(os.path.join(mirror_dir, mf))]
        mirror_subfolders = [msf for msf in os.listdir(mirror_dir)
                             if os.path.isdir(os.path.join(mirror_dir, msf))]

        # Detects new stuff
        new_files = set(filenames) - set(mirror_filenames)
        new_subfolders = set(subfolders) - set(mirror_subfolders)
        curtain()
        print("original", subfolders)
        print("mirror", mirror_subfolders)
        print("new:", new_subfolders)
        curtain()

        # updates new stuff
        local_new_files = []
        for nf in new_files:
            print("source:", source)
            print("fileO", os.path.join(active_dir, nf))
            print("dirDest", dest)
            print("mirror:", mirror_dir)
            shutil.copy2(os.path.join(active_dir, nf), mirror_dir)
            local_new_files.append(nf)
            files_added.update({mirror_dir: local_new_files})

        local_new_sub_folders = []
        for nsf in new_subfolders:
            # todo a function that copies a folder and all its contents
            # todo idea: mkdir and then shutil.copytree?
            print("orig fold:", os.path.join(active_dir, nsf))
            print("dest fold:", mirror_dir)
            new_dir = os.path.join(mirror_dir, nsf)
            #os.makedirs(new_dir)
            shutil.copytree(os.path.join(active_dir, nsf), new_dir)
            dir_added.append(nsf)



        #debugs
        print("filenames:", filenames)
        print("mirror files:", mirror_filenames)
        print("new files:", new_files)

    # Reports changes
    print("The following subfolders have been added with their content:")
    for f in dir_added:
        print("\t", f)

    for k in files_added:
        print("new addition in " + k + ":")
        for file in files_added[k]:
            print("\t" + file)


if __name__ == "__main__":
    t_source = os.path.join("C:\\", "Users", "pgmic", "Desktop", "Start_bak")
    t_dest = os.path.join("C:\\", "Users", "pgmic", "Desktop", "CT_test")
    update_bak(t_source, t_dest)

# TODO clean from debug detecting and adding new file and folders
# TODO replace the hardcoded text in Report changes
