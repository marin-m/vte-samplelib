# vte-samplelib

This repository contains an additional package to [vmlinux-to-elf](https://github.com/marin-m/vmlinux-to-elf) meant to construct a database of kernel versions, architecture, interesting files (DONE), of Debian relases (DONE), and perform C/I for `vmlinux-to-elf` over a database of samples (TODO, cf. https://github.com/marin-m/vte-samplelib/issues/3)

Use `uv sync` to create a local `.venv` and/or `uv tool install -e .` to make the script commands in `vte_samplelib/scripts` usable locally (in `~/.local/bin` with a symlink to the source directory).

> TODO: ~~Make a simple web frontend with Flask?~~ Use Github actions for the C/I for the moment

> TODO: Use samples sorted within folders with symlink (by-version, by-architecture, etc.)?

## DONE: Tools to populate a reusable kernel+kernel assets+Debian versions database

Here are the commands you can run to populate the SQLite database:

```
sudo apt install sqlitebrowser git python3
sudo snap install astral-uv
cd
git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
git clone git@github.com:marin-m/vte-samplelib.git
cd vte-samplelib/
uv sync
source .venv/bin/activate
cp config.toml.sample config.toml
nano config.toml
samplelib-extract-info
samplelib-populate-debian-info
sqlitebrowser database.sqlite3
```

## TODO: Utils to write proposals

See https://github.com/marin-m/vte-samplelib/issues/3
```
