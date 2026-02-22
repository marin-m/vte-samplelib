# vte-samplelib

This repository contains an additional package to [vmlinux-to-elf](https://github.com/marin-m/vmlinux-to-elf) meant to construct a database of kernel versions, architecture, interesting files (DONE), of Debian relases (DONE), to sort out available kernel samples (TODO), provide CI/CD (TODO), generate kernel blobs with and without symbols from scratch (TODO)

Work-in-process: Make a CI/CD-alike pipeline to **build kernels and generate usable test samples**

Cf. http://synology-marin/mediawiki/index.php/Vmlinux-to-elf/Samples_library

Use `uv sync` to create a local `.venv` and/or `uv tool install -e .` to make the script commands in `vte_samplelib/scripts` usable locally (in `~/.local/bin` with a symlink to the source directory).

> TODO: Make a simple web frontend with Flask?

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

Exectuable scripts specifications:

* `sample_manager.py`

```
sample_manager.py {list,add,rm,reorganize}
  list
  add <readable_name> <file_path> [<file_path> [..]]
  rm <readable_name|readable_name/relative_path|file_path>
    => will confirm actions
    => may allow to remove individual samples AND automatically change file rotation?
  reorganize
    => will just automatically ensure that everyone in the directory structure is conformant to the specification below, maybe regenerate in chain Image,kallsyms/vmlinux-output, and cleanup if needed?
    should also be triggered locally by add/rm in one sense
```

```
filetype_detector.py
XX
```

```
kernel_setup.py
XX
```

XX

Module libraries specifications:

XX

## Directory structure proposal

```
samples/
```

```
samples/kernel/<readable_name>/{kallsyms-original,{vmlinuz,vmlinux,android.boot,bzImage},Image,kallsyms-output-DATE-COMMITHASH~dirty,kallsyms-output-DATE-COMMITHASH,kallsyms-output-DATE-COMMITHASH.bak,kallsyms-output-DATE-COMMITHASH.bak.1,vmlinux-output-DATE-COMMITHASH~dirty,vmlinux-output-DATE-COMMITHASH,vmlinux-output-DATE-COMMITHASH.bak,vmlinux-output-DATE-COMMITHASH.bak.1}

# {Image} may be generated from {vmlinuz,vmlinux,android.boot,bzImage}
# {vmlinux-output-DATE-COMMITHASH~dirty,vmlinux-output-DATE-COMMITHASH,vmlinux-output-DATE-COMMITHASH.bak,vmlinux-output-DATE-COMMITHASH.bak.1...} will be generated whenever output from vmlinux-to-elf changes (keeping the older disk timestamp of the file, adding a commuit hash + the state of the git Tree? fail if not in a git tree)
# ⚠️ we should then design FIRST design a FILE TYPE DETECTOR routine?
# ⚠️ HOW TO MANAGE
# (that we will then be able to import into the main project, etc.)?

samples/by-version/<version>/<symlink_to_readable_name>
samples/by-arch/<arch>/<symlink_to_readable_name>
samples/by-compression/<compression:bz2|gzip|zstd|lz4|lzo|etc>/<symlink_to_readable_name>

samples/by-version-arch/<arch>/<version>/<symlink_to_readable_name>
samples/by-arch-arch/<version>/<arch>/<symlink_to_readable_name>
```


## What should I do?

* ⚠️ put the kernel Git tree at a static/known location? (What about having nested trees? should we avoid it?)
  * In order to correctly organize, it is likely that we should
    * Have the Linux kernel Git tree in a known place like `$HOME/vte-kernel-tree` (clone it if absent)
    * When cross-compiling a kernel, COPY THE TREE in another DYNAMICALLY CREATED (BY DEFAULT TEMPORARY?) directory and CLEAN IT UP (rm EXCEPT IF THERE IS A --KEEP option) afterwards
    * COPY THE OUTPUT FILES + MEMORY OF THE LS -L OVER THE OUTPUT KERNEL CLEANLY
    * Support **DOING THE COMPILATION OVER SSH**?
    * **TASK MANAGE COMPILATION IN A LOCAL SQLITE DB WITH A STATE?**
* ⚠️ keep a local .toml file regarding this matter?
* ⚠️ document deeper about pyproject.toml? etc
  * See
     * https://github.com/marin-m/vmlinux-to-elf/pull/79
     * https://packaging.python.org/en/latest/tutorials/packaging-projects/
     * https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
        * Maybe use the black linter too?
     * https://toml.io/en/

* ⚠️ USE BUILDROOT?
  * https://buildroot.org/

* => https://linuxembedded.fr/2024/06/yocto-vs-buildroot-vs-everyone-else
* => https://buildroot.org/downloads/manual/manual.html#_about_buildroot
* => https://buildroot.org/download.html

==> **SSH over Zbook Manjaro and use it as a remotely-controlled build server?**

## What did I do earlier?

For memory:

```
03:30:24:marin:~/vte-samplelib$ du -sh ~/vte-tests/linux-5.13.9/
2.4G	/home/marin/vte-tests/linux-5.13.9/
```

The final output of the ARM64 build process is:

```
05:14:28:marin:~/vte-samplelib$ ls -lhrtA /home/marin/vte-tests/linux-5.13.9/
(..)
drwxrwxr-x 140 marin marin 4.0K Oct 19 03:49 drivers
-rw-rw-r--   1 marin marin  29K Oct 19 03:49 modules.order
-rw-rw-r--   1 marin marin  398 Oct 19 03:49 .modules.order.cmd
-rw-rw-r--   1 marin marin    2 Oct 19 03:49 .version
-rw-rw-r--   1 marin marin 231M Oct 19 03:49 vmlinux.o
-rw-rw-r--   1 marin marin 679K Oct 19 03:49 vmlinux.symvers
-rw-rw-r--   1 marin marin 200K Oct 19 03:49 modules.builtin.modinfo
-rw-rw-r--   1 marin marin  36K Oct 19 03:49 modules.builtin
05:16:17:marin:~/vte-samplelib$ file /home/marin/vte-tests/linux-5.13.9/vmlinux.o
/home/marin/vte-tests/linux-5.13.9/vmlinux.o: ELF 64-bit LSB relocatable, ARM aarch64, version 1 (SYSV), with debug_info, not stripped
```

The commands followed were from: https://github.com/marin-m/vmlinux-to-elf/issues/67

```
$ git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
$ cd linux
$ git checkout v5.13
$ make CROSS_COMPILE=aarch64-linux-gnu- ARCH=arm64 KERNEL_LZ4=y -j defconfig
$ make CROSS_COMPILE=aarch64-linux-gnu- ARCH=arm64 KERNEL_LZ4=y -j
```
