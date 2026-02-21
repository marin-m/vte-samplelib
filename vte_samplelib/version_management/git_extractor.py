#!/usr/bin/python3
#-*- encoding: Utf-8 -*-

"""
    This script XX

    * http://synology-marin/mediawiki/index.php?title=Vmlinux-to-elf/Planned_modules/Shared_database
    * http://synology-marin/mediawiki/index.php?title=Vmlinux-to-elf/Planned_modules/Linux_kernel_version_DB
    * http://synology-marin/mediawiki/index.php?title=Vmlinux-to-elf/Samples_library/Linux_2.6.10_from_Ubuntu_5.04

        => Perhaps I don't need to parse anything from Wikipedia and everything I should look at is in Git/FTP ?

                ==> https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Makefile
                        => Tags are dated
                    => All tags
                        => https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/refs/?h=v6.19
                    
                https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/Makefile?h=v6.19
                    => https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/process/changes.rst?h=v6.19
                            (Document/Changes is still here but just a symlink to process/changes.rst in recent kernels)
                                => https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/Documentation/process/changes.rst?h=v6.19
                        => https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/snapshot/linux-6.19.tar.gz
                                
                    Oldest kernel in Git:
                    => https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Makefile?h=v2.6.12
                        => https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/Changes?h=v2.6.12
                        => https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/snapshot/linux-2.6.12.tar.gz

                        Pre-git kernel example:
                            => https://www.kernel.org/pub/linux/kernel/v2.6/
                                => https://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.10.tar.xz
                                    => (Documentation/Changes w/ table + Makefile of kernel + moddate of Makefile are here)
            
            => Should I retrieve refs from the kernel Git tree over HTTPS?
                Or just clone the whole kernel tree?

                    "The git protocol is a special daemon that comes packaged with Git; it listens on a dedicated port
                     (9418) that provides a service similar to the SSH protocol, but with absolutely no authentication."
                        Cf. https://stackoverflow.com/questions/33846856/what-exactly-is-the-git-protocol

                            time git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
                                => Cloned real	6m40,658s user	15m7,114s sys	1m47,165s
                                    Cf. https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/?h=v6.19

                        19:37:12:marin:~$ du -sh linux
                            5.3G	linux
            
                            https://stackoverflow.com/questions/18995854/how-can-i-use-github-api-to-get-all-tags-or-releases-for-a-project

                            http://developer.github.com/v3/git/refs/
                                GET /repos/:owner/:repo/git/refs/tags
                            
                                $ git tags


                                https://docs.github.com/en/rest/git/tags?apiVersion=2022-11-28#get-a-tag
                                  https://api.github.com/repos/OWNER/REPO/git/tags/TAG_SHA
                
            !!
                https://api.github.com/repos/torvalds/linux/git/refs/tags
                    => https://api.github.com/repos/torvalds/linux/git/tags/26791a8bcf0e6d33f43aef7682bdb555236d56de
                        => https://api.github.com/repos/torvalds/linux/git/commits/9ee1c939d1cb936b1f98e8d81aeffab57bae46ab
                            => date	"2005-06-17T19:48:29Z"


                https://gitpython.readthedocs.io/en/stable/tutorial.html

                        = ⚠️=> GitPython provides object model access to your git
                          repository. This tutorial is composed of multiple sections,
                          most of which explain a real-life use case.

        => Perhaps I will need to build a SQLite database only much later than now and I should focus on
           outputting minimally viable JSON (or CSV) output?

    WIP 2025-01-25
"""

# from vte_samplelib.core.database import (
#     KernelRelease, KernelReleaseDependency
# )

from re import search, IGNORECASE

from vte_samplelib.core.database import (
    KernelVersion,
    KernelVersionDependency,
    KernelRelevantFile,
)

from git import Tree, Blob

# https://en.wikipedia.org/wiki/Linux_kernel_version_history

# https://www.kernel.org/pub/linux/kernel/ (use FTP for enumeration?)
#  * https://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.10.tar.xz


# => 2026-02-19  PERHAPS USE JSON/CSV OR PROTO OUTPUT BEFORE IMPORTING ANYTHING TO SQLITE ?


# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/
# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/Changes?h=v2.6.12
# = https://github.com/torvalds/linux/blob/v2.6.12/Documentation/Changes
# (kernel not versioned on Git earlier)

# Sample kernel requirements (recent): https://github.com/torvalds/linux/blob/v6.19-rc7/Documentation/process/changes.rst

# Sample kernel requirements (old): https://github.com/torvalds/linux/blob/v2.6.19/Documentation/Changes

REMOTE_URL = 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/'
TREE_URL = REMOTE_URL + 'tree/%s?id=%s'
"""
class ExtraGitParser:

    pass # XX wip
"""

class ChangelogParser:

    def __init__(self, tree : Tree, kernel : KernelVersion):

        changelog_file = tree['Documentation/Changes']

        if changelog_file.mode == Blob.link_mode:
            changelog_file = tree['Documentation/process/changes.rst']

        try:
            text = changelog_file.data_stream.read().decode('utf-8')
        except UnicodeDecodeError:
            text = changelog_file.data_stream.read().decode('cp1252')

        lines = text.splitlines(keepends = False)

        dep = KernelRelevantFile()
        dep.release = kernel
        dep.file_name = changelog_file.path
        # dep.data = text
        dep.architecture_code = None
        dep.vcs_browser_url = TREE_URL % (dep.file_name, kernel.version_string)
        dep.save()

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

                    dep = KernelVersionDependency()
                    dep.release = kernel
                    dep.dependency_name = progname.replace('(optional)', '').strip()
                    dep.minimal_version = progver
                    dep.base_command = progcmd.split(' ')[0]
                    dep.version_command = progcmd
                    dep.dependency_is_optional = '(optional)' in progname
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

# xx wip