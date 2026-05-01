% MYTOOL(1) mytool 0.0.1
% Your Name
% 2026

# NAME

mytool - example CLI scaffolded from the cli-tool guideline

# SYNOPSIS

**mytool** \[*global-flags*\] *subcommand* \[*flags*\] \[*args*\]

# DESCRIPTION

**mytool** demonstrates the layout recommended by the
*cli-tool* guideline: a thin entry point, one subcommand per
file, shell completions for bash/zsh/fish, and a man page
generated from this Markdown source.

Replace this description with one that fits your own tool.

# COMMANDS

**foo** \[*name*\]
:   Greet someone. *name* defaults to *world*.

**bar** \[**--count** *n*\]
:   Print a counter *n* times. Defaults to 1.

**completion** *shell*
:   Print shell-completion script for *bash*, *zsh*, *fish*, or
    *powershell*. Redirect to the right file under
    **completions/** and source from your shell rc.

**version**
:   Print version, commit, and build date.

# OPTIONS

**-h**, **--help**
:   Show help and exit.

**--version**
:   Show version and exit.

# EXIT STATUS

*0*
:   Success.

*1*
:   Generic failure.

*2*
:   Usage error (bad flags or args).

# FILES

*~/.config/mytool/config.yaml*
:   User configuration (XDG on Linux/macOS).

# SEE ALSO

**git**(1), **gh**(1), **kubectl**(1)

# BUGS

Report at <https://github.com/example/mytool/issues>.

# RENDERING

Convert this file to a real man page with:

```
pandoc -s -t man docs/manpage.md -o docs/mytool.1
```

Install **mytool.1** under */usr/local/share/man/man1/* (or use
your packaging tool's MANDIR convention).
