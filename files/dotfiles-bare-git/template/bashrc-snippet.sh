# bashrc-snippet.sh
#
# Append this single line to ~/.bashrc (or ~/.zshrc) to define the `dotfiles`
# command used by the bare-git pattern. setup.sh does this automatically.
#
# After adding, `source ~/.bashrc` (or open a new shell) and run:
#   dotfiles status
#
# If `which git` returns something other than /usr/bin/git on your system
# (Homebrew, asdf, mise), substitute the right absolute path or use plain `git`.

alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
