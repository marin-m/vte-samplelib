#!/usr/bin/env python3
#-*- encoding: Utf-8 -*-
from argparse import ArgumentParser

# TODO use Paramiko when SSH is enabled in config?

"""
    => How to reproduce building a kernel manually? (Commands)

    sudo apt install XX toolchains ? (for ARM64, depends on: gcc-aarch64-linux-gnu
        Cf. https://unix.stackexchange.com/questions/657882/how-do-i-cross-compile-the-linux-kernel)
    
        "For raw kernels, the following architectures can be detected (using magics from binwalk):
          MIPSEL, MIPSEB, ARMEL, ARMEB, PowerPC, SPARC, x86, x86-64, ARM64, MIPS64, SuperH, ARC.

        ⚠️ The MIPS GCC cross-compiler was removed from Ubuntu 25.10 repositories
        SuperH => gcc-sh4-linux-gnu
        ARC => gcc-arc-linux-gnu

        ⚠️ USE BUILDROOT Instead of APT?
        https://buildroot.org/ => LTS https://buildroot.org/downloads/buildroot-2025.02.8.tar.xz

        => ℹ️ NEXT STEP: Build a 2.6.10 kernel for x86 on our local machine?
        
          Cf. https://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.10.tar.xz
          https://wiki.archlinux.org/title/Kernel/Traditional_compilation
          "After completing all steps above, you should have the following 3 files and 1 soft symlink in your /boot directory along with any other previously existing files:
            Kernel: vmlinuz-linuxAB
            Initramfs: initramfs-linuxAB.img
            System Map: System.map-linuxAB
            System Map kernel symlink: System.map (which symlinks to System.map-linuxAB)"
          
        => ℹ️ prefer QEMU/KVM (or libvirt) if we need an older Ubuntu/Arch/.. to compile to MIPS etc.?

          => No graphical environment: Simpler/less memory?

        => https://linuxembedded.fr/2024/06/yocto-vs-buildroot-vs-everyone-else
        => https://buildroot.org/downloads/manual/manual.html#_about_buildroot
        => https://buildroot.org/download.html

        https://news.slashdot.org/story/24/04/29/2325210/t2-linux-245-released
        "T2 is known for its sophisticated cross compile support and support for nearly all existing
         CPU architectures: Alpha, Arc, ARM(64), Avr32, HPPA(64), IA64, M68k, MIPS(64), Nios2, PowerPC(64)(le),
         RISCV(64), s390x, SPARC(64), and SuperH x86(64). T2 is an increasingly popular choice for embedded
         systems and virtualization. It also still supports the Sony PS3, Sgi, Sun and HP workstations, as
         well as the latest ARM64 and RISCV64 architectures."
        https://t2linux.com/download/25.10?download/
        https://dl.t2sde.org/binary/2025/t2-25.10-x86-64-base-wayland-glibc-gcc-nocona.iso

        => ➡️ https://t2linux.com/handbook/html/t2-book.html

        => Maybe Buildroot does not support all target architectures?

        "Buildroot knows about a number of well-known cross-compilation toolchains
        (from Linaro for ARM, Sourcery CodeBench for ARM, x86-64, PowerPC, and MIPS"

        ⚠️ What is the first version we should build?

        (XX WIP:
        
        )

        https://askubuntu.com/questions/873278/linux-kernel-version-and-gcc-version-match

        And Documentation/Changes gives a list of required versions of GCC (listed as "GNU C") and the other build dependencies for Linux, as well as how to check what version of each you currently have installed:

        => https://www.kernel.org/doc/Documentation/Changes

        ====================== ===============  ========================================
        Program        Minimal version       Command to check the version
        ====================== ===============  ========================================
        GNU C                  8.1              gcc --version
        Clang/LLVM (optional)  15.0.0           clang --version
        Rust (optional)        1.78.0           rustc --version
        bindgen (optional)     0.65.1           bindgen --version
        GNU make               4.0              make --version
        bash                   4.2              bash --version
        binutils               2.30             ld -v
        flex                   2.5.35           flex --version
        bison                  2.0              bison --version
        pahole                 1.16             pahole --version
        util-linux             2.10o            mount --version
        kmod                   13               depmod -V
        e2fsprogs              1.41.4           e2fsck -V
        jfsutils               1.1.3            fsck.jfs -V
        xfsprogs               2.6.0            xfs_db -V
        squashfs-tools         4.0              mksquashfs -version
        btrfs-progs            0.18             btrfs --version
        pcmciautils            004              pccardctl -V
        quota-tools            3.09             quota -V
        PPP                    2.4.0            pppd --version
        nfs-utils              1.0.5            showmount --version
        procps                 3.2.0            ps --version
        udev                   081              udevd --version
        grub                   0.93             grub --version || grub-install --version
        mcelog                 0.6              mcelog --version
        iptables               1.4.2            iptables -V
        openssl & libcrypto    1.0.0            openssl version
        bc                     1.06.95          bc --version
        Sphinx\ [#f1]_         3.4.3            sphinx-build --version
        GNU tar                1.28             tar --version
        gtags (optional)       6.6.5            gtags --version
        mkimage (optional)     2017.01          mkimage --version
        Python                 3.9.x            python3 --version
        GNU AWK (optional)     5.1.0            gawk --version
        ====================== ===============  ========================================

        ====================== ===============  ========================================
                Program        Minimal version       Command to check the version
        ====================== ===============  ========================================
        GNU C                  3.2              gcc --version
        GNU make               3.80             make --version
        binutils               2.12             ld -v
        util-linux             2.10o            fdformat --version
        module-init-tools      0.9.10           depmod -V
        e2fsprogs              1.41.4           e2fsck -V
        jfsutils               1.1.3            fsck.jfs -V
        reiserfsprogs          3.6.3            reiserfsck -V
        xfsprogs               2.6.0            xfs_db -V
        squashfs-tools         4.0              mksquashfs -version
        btrfs-progs            0.18             btrfsck
        pcmciautils            004              pccardctl -V
        quota-tools            3.09             quota -V
        PPP                    2.4.0            pppd --version
        isdn4k-utils           3.1pre1          isdnctrl 2>&1|grep version
        nfs-utils              1.0.5            showmount --version
        procps                 3.2.0            ps --version
        oprofile               0.9              oprofiled --version
        udev                   081              udevd --version
        grub                   0.93             grub --version || grub-install --version
        mcelog                 0.6              mcelog --version
        iptables               1.4.2            iptables -V
        openssl & libcrypto    1.0.0            openssl version
        bc                     1.06.95          bc --version
        Sphinx\ [#f1]_         1.2              sphinx-build --version
        ====================== ===============  ========================================

        .. [#f1] Sphinx is needed only to build the Kernel documentation

        The following kernel compression formats can be automatically detected: XZ, LZMA, GZip, BZ2, LZ4, LZO and Zstd."

        "It should support kernels from version 2.6.10 (December 2004), until the current 6.4
          (as of August 2023). Only kernels explicitly configured without CONFIG_KALLSYMS
          should not be supported. If this kernel configuration variable was not set at
          build, then you will get: KallsymsNotFoundException: No embedded symbol table
          found in this kernel."

    Cf. Github issue: https://github.com/marin-m/vmlinux-to-elf/issues/67

        $ git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
        $ cd linux
        $ git checkout v5.13
        $ make CROSS_COMPILE=aarch64-linux-gnu- ARCH=arm64 KERNEL_LZ4=y -j defconfig
        $ make CROSS_COMPILE=aarch64-linux-gnu- ARCH=arm64 KERNEL_LZ4=y -j

        05:14:28:marin:~/boisse-samplelib$ ls -lhrtA /home/marin/boisse-tests/linux-5.13.9/
        (..)
        drwxrwxr-x 140 marin marin 4.0K Oct 19 03:49 drivers
        -rw-rw-r--   1 marin marin  29K Oct 19 03:49 modules.order
        -rw-rw-r--   1 marin marin  398 Oct 19 03:49 .modules.order.cmd
        -rw-rw-r--   1 marin marin    2 Oct 19 03:49 .version
        -rw-rw-r--   1 marin marin 231M Oct 19 03:49 vmlinux.o
        -rw-rw-r--   1 marin marin 679K Oct 19 03:49 vmlinux.symvers
        -rw-rw-r--   1 marin marin 200K Oct 19 03:49 modules.builtin.modinfo
        -rw-rw-r--   1 marin marin  36K Oct 19 03:49 modules.builtin

        => (Maybe document a bit about Ansible out of curiosity?
            No, we know Paramiko better and not managing a centralized infrastructure)
"""

## XX WIP
