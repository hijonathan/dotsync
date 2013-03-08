Dotsync: Easy file syncing and preservation
===========================================

Dotsync helps you create symbolic links to files that you want to protect or backup. It's great for preferences files that can't be moved into a Dropbox. Rather than managing these symbolic links yourself, Dotsync does it for you.


## Notable Features


#### `dotsync add`

Add files and folders you want dotsync to track.

    > dotsync add ~/.gitconfig
    > dotsync add ~/.oh-my-zsh/custom

#### `dotsync status`

When you need to know what things are tracked, you can simply ask dotsync.

    > dotsync status
    ~/.gitconfig -> ~/path/to/backup/.gitconfig                UNTRACKED
    ~/.oh-my-zsh/custom -> ~/path/to/backup/.oh-my-zsh/custom  UNTRACKED

#### `dotsync save`

When you're ready, tell dotsync to copy them to your new location and replace the old versions with symbolic links.

    > dotsync save
    > dotsync status
    ~/.gitconfig -> ~/path/to/backup/.gitconfig                TRACKED
    ~/.oh-my-zsh/custom -> ~/path/to/backup/.oh-my-zsh/custom  TRACKED

#### `dotsync remove`

Got too carried away? Tell dotsync to put a file back where it found it.

    > dotsync remove ~/.ssh

#### `dotsync restore`

Starting from a new machine and need to get back your dotfiles? This is what dotsync was made for.

    > dotsync restore ~/path/to/backup/dotsync.yaml


## TODO

- Tight github integration with save/restore.

## Acknowledgements

@tpetr for creating HubSpot/moxie, upon which the structure of this code is based.

United Airlines flight #357 for being excruciatingly long and wifi-less.
