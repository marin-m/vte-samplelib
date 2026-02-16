#!/usr/bin/python3
#-*- encoding: Utf-8 -*-

"""
    This script XX

    * http://synology-marin/mediawiki/index.php?title=Vmlinux-to-elf/Planned_modules/Shared_database
    * http://synology-marin/mediawiki/index.php?title=Vmlinux-to-elf/Planned_modules/Linux_kernel_version_DB
    * http://synology-marin/mediawiki/index.php?title=Vmlinux-to-elf/Samples_library/Linux_2.6.10_from_Ubuntu_5.04

    WIP 2025-01-25
"""

from vmlinux_to_elf_samplelib.core.database import (
    KernelRelease, KernelReleaseDependency
)

from re import search, IGNORECASE

# https://en.wikipedia.org/wiki/Linux_kernel_version_history

# https://www.kernel.org/pub/linux/kernel/ (use FTP for enumeration?)
#  * https://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.10.tar.xz

# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/
# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/Changes?h=v2.6.12
# = https://github.com/torvalds/linux/blob/v2.6.12/Documentation/Changes
# (kernel not versioned on Git earlier)

# Sample kernel requirements (recent): https://github.com/torvalds/linux/blob/v6.19-rc7/Documentation/process/changes.rst

# Sample kernel requirements (old): https://github.com/torvalds/linux/blob/v2.6.19/Documentation/Changes

class ChangelogParser:

    def __init__(self):

        xx # Use GIT + regexes

        lines = text.splitlines(keepends = False)

        reached_gnuc_verspec = False

        PATTERN = r'(GNU C {2,})(\d[^ ]* {2,}).*?(gcc --version.*)'

        for line in lines:
            if not reached_gnuc_verspec:
                res = search(PATTERN, line, flags = IGNORECASE)

                if res:
                    (progname_start, progname_end) = res.span(1)
                    (progver_start, progver_end) = res.span(2)
                    (progcmd_start, progcmd_end) = res.span(3)
                    reached_gnuc_verspec = True
            
            if reached_gnuc_verspec:
                if line.strip():
                    progname = line[progname_start:progname_end].rstrip()
                    progver = line[progver_start:progver_end].rstrip()
                    progcmd = line[progcmd_start:].rstrip()

                    dep = KernelReleaseDependency.create(XX
                    dep.save()
                                                   
                    # XX links things
                    # XX save things to database
                    # XX avoid duplicates/purge table before feeding database again?
                    #   or (safer in case of bug) just ignore existing DB entries with the same Linux version key/name ?
                
                else:
                    break
            
        if not reached_gnuc_verspec:
            pass # xx throw rror


        pass # todo

class WikipediaFetcher:

    pass # todo # Use REST API + regex

    # Do:
    # KernelRelease.create(XX)
    # KernelReleaseDependency.create(XX)
    # (See: https://docs.peewee-orm.com/en/latest/peewee/quickstart.html)

class FTPFetcher:

    pass # todo

# xx wip