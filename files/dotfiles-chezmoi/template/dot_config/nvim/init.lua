-- dot_config/nvim/init.lua — minimal Neovim config stub.
--
-- Source path: ~/.local/share/chezmoi/dot_config/nvim/init.lua
-- Target path: ~/.config/nvim/init.lua
--
-- This is a literal (non-templated) file. Replace with your own Neovim
-- configuration. Add .tmpl and rename to init.lua.tmpl if you need
-- per-machine variation.

vim.opt.number         = true
vim.opt.relativenumber = true
vim.opt.expandtab      = true
vim.opt.shiftwidth     = 2
vim.opt.tabstop        = 2
vim.opt.smartindent    = true
vim.opt.termguicolors  = true
vim.opt.clipboard      = 'unnamedplus'

-- Leader key
vim.g.mapleader = ' '

-- Quick save / quit
vim.keymap.set('n', '<leader>w', ':w<CR>')
vim.keymap.set('n', '<leader>q', ':q<CR>')
