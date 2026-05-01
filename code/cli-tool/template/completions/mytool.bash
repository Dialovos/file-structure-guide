# bash completion for mytool.
#
# Regenerate from the binary:
#     mytool completion bash > completions/mytool.bash
#
# Install for the current user:
#     mkdir -p ~/.local/share/bash-completion/completions
#     cp completions/mytool.bash ~/.local/share/bash-completion/completions/mytool
#
# System-wide (Linux):
#     sudo cp completions/mytool.bash /etc/bash_completion.d/mytool
#
# This stub is replaced at release time by the real cobra-generated
# script. Keeping a placeholder in the repo means downstream
# packagers can install the file path even before the first release.

_mytool_completions() {
  COMPREPLY=()
  return 0
}

complete -F _mytool_completions mytool
