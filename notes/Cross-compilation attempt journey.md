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
