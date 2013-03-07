import os


HOME_DIR = '/Users/jonathankim'
FILES_TO_IGNORE = [
    '.DS_Store'
]


dotfiles_dir = os.path.join(os.getcwd(), 'files')
backup_dir = os.path.join(os.getcwd(), 'backup')


def sync():
    dotfiles = filter(lambda x: x not in FILES_TO_IGNORE, os.listdir('files'))

    for file_name in dotfiles:
        dotfile_path = os.path.join(dotfiles_dir, file_name)
        home_path = get_file_path(file_name)

        copy_existing(home_path, backup_dir)
        remove_existing(home_path)

        make_symlink(dotfile_path, home_path)


def get_file_path(file_name):
    path_parts = file_name.split(':')
    return os.path.join(HOME_DIR, os.path.join(*path_parts))


def copy_existing(source_path, destination_path):
    if not os.path.exists(destination_path) or not os.path.isdir(destination_path):
        os.mkdir(destination_path)
        print ('INFO: Created new dir at %s') % destination_path

    contents = ''
    with open(source_path) as f:
        contents = f.read()

    copied_file_name = make_file_name(source_path)
    copied_file_path = os.path.join(destination_path, copied_file_name)
    with open(copied_file_path, 'w') as f:
        f.write(contents)

    print ('INFO: Copied %s as %s') % (source_path, copied_file_path)

    return


def make_file_name(file_path):
    path_parts = file_path.replace(HOME_DIR + '/', '').split('/')
    return ':'.join(path_parts)


def remove_existing(target_path):
    print ('INFO: Removed file at %s' % (target_path))
    os.remove(target_path)
    return


def make_symlink(source_path, target_path):
    try:
        print ('SUCCESS: Created a symlink between %s and %s' % (source_path, target_path))
        os.symlink(source_path, target_path)
    except:
        print ('FAILURE: Couldn\'t symlink %s and %s' % (source_path, target_path))
        pass

    return


if __name__ == '__main__':
    sync()
