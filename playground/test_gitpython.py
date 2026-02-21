#!/usr/bin/env python3
# -*- encoding: Utf-8 -*-
from os import environ

environ['GIT_PYTHON_TRACE'] = 'full'
from logging import basicConfig, INFO

basicConfig(level=INFO)

# import vte_samplelib.pb.re.fossplant.vte_samplelib.kernel_version_db_pb2 as pb
# pb.KernelRelevantFile

from git import Repo, Blob

KERNEL_DIR = '/home/marin/linux'

# Cf. https://gitpython.readthedocs.io/en/stable/tutorial.html
# WIP

repo = Repo(KERNEL_DIR)

"""
    NOTE:
        https://gitpython.readthedocs.io/en/stable/quickstart.html#clone-from-url
        
            We even have:
                repo_url = "https://github.com/gitpython-developers/QuickStartTutorialFiles.git"

                repo = Repo.clone_from(repo_url, local_dir)

                # repo = git.Repo.clone_from(self._small_repo_url(), os.path.join(rw_dir, "repo"), branch="master")

                # "An Object is anything storable in git’s object database. Objects contain information about their type, their uncompressed size as well as the actual data. Each object is uniquely identified by a binary SHA1 hash, being 20 bytes in size, or 40 bytes in hexadecimal notation.

                # Git only knows 4 distinct object types being Blobs, Trees, Commits and Tags."

                # "Index objects are objects that can be put into git’s index. These objects are trees, blobs and submodules which additionally know about their path in the file system as well as their mode.

                self.assertEqual(hct.path, "")  # Root tree has no path.
                assert hct.trees[0].path != ""  # The first contained item has one though.
                self.assertEqual(hct.mode, 0o40000)  # Trees have the mode of a Linux directory.
                self.assertEqual(hct.blobs[0].mode, 0o100644)  # Blobs have specific mode, comparable to a standard Linux fs.

                Access blob data (or any object data) using streams.

                hct.blobs[0].data_stream.read()  # Stream object to read data from."

                # assert len(tree.trees) > 0  # Trees are subdirectories.
                assert len(tree.blobs) > 0  # Blobs are files.
                assert len(tree.blobs) + len(tree.trees) == len(tree)

                # "self.assertEqual(tree["smmap"], tree / "smmap")  # Access by index and by sub-path.
                for entry in tree:  # Intuitive iteration of tree members.
                    print(entry)
                blob = tree.trees[1].blobs[0]  # Let's get a blob in a sub-tree.
                assert blob.name
                assert len(blob.path) < len(blob.abspath)
                self.assertEqual(tree.trees[1].name + "/" + blob.name, blob.path)  # This is how relative blob path generated.
                self.assertEqual(tree[blob.path], blob)  # You can use paths like 'dir/file' in tree,

                There is a convenience method that allows you to get a named sub-object from a tree with a syntax similar to how paths are written in a posix system

                assert tree / "smmap" == tree["smmap"]
                assert tree / blob.path == tree[blob.path]"

                # "As trees allow direct access to their intermediate child entries only, use the traverse method to obtain an iterator to retrieve entries recursively

                assert len(tree) < len(list(tree.traverse()))"

    TODO:
        We should extract metadata laid like this:

        {
            "kernels": [
                {
                    "tag": "v2.6.12",
                    "commit": "9ee1c939d1cb936b1f98e8d81aeffab57bae46ab",
                    (
                    "commit_author_date": "2005-06-17 12:48:29-07:00"
                    "commit_committer_date": "2005-06-17 12:48:29-07:00",
                    OR
                    "http_lastmod_date"
                    )
                },
                .. WIP
            ]
        }
"""

"""
print(dir(repo.tags[0]), dir(repo.tags[0].object))
print()
print(repo.tags[0].object.type)
print(repo.tags[0].object.object.type)
print()
print(repo.tags[9].object.type)
print(repo.tags[9].object.object.type)
print()
print(dir(repo.tags[9]), dir(repo.tags[9].object))
print()
print(dir(repo.tags[9]), dir(repo.tags[9].commit))
print()
print(repo.tags[9].commit.committed_datetime, '/', repo.tags[9].commit.authored_datetime)
exit()
"""


def print_blob(blob):
    print(
        '=>',
        blob.mime_type,
        'link=%s' % bool(blob.mode == blob.link_mode),
        '%dk' % (blob.size / 1024),
        blob.path,
        oct(blob.mode),
        blob.data_stream.read(196),
    )


for tag_ref in repo.tags:
    tag = tag_ref.object
    tag_object = tag.object

    print(f'[{tag_ref.path} tag={tag.tag} ref={tag.hexsha}]')
    if tag_object.type == 'commit':
        # if tag_object.committed_datetime != tag_object.authored_datetime:
        #     print('  WARNING MISMATCHING DATES')
        print(
            f'  [commit ref={tag_object.hexsha} committed_datetime={tag_object.committed_datetime} authored_datetime={tag_object.authored_datetime}]'
        )
        tree = tag_object.tree
        print(f'    [tree ref={tree.hexsha}]')
        print(
            f'      [{[x.path for x in tree.trees]}] [{[x.path for x in tree.blobs]}]'
        )
        print('TREE CONTAINS', len(tree.list_traverse()), 'OBJECTS')
        print_blob(tree / 'Makefile')
        print_blob(tree / 'Documentation/Changes')
        if tree['Documentation/Changes'].mode == Blob.link_mode:
            print_blob(tree / 'Documentation/process/changes.rst')
        print_blob(tree['kernel/kallsyms.c'])
        print_blob(tree['scripts/kallsyms.c'])
        try:
            print_blob(tree['arch/arm64/include/asm/elf.h'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/s390/include/asm/elf.h'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/x86/include/asm/elf.h'])
        except KeyError:
            pass
        try:
            print_blob(tree['include/asm-i386/elf.h'])
        except KeyError:
            pass
        try:
            print_blob(tree['include/asm-s390/elf.h'])
        except KeyError:
            pass
        try:
            print_blob(tree['scripts/kallsyms'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/x86/boot/header.S'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/x86/boot/compressed/vmlinux.lds.S'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/x86/boot/compressed/Makefile'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/arm64/kernel/.vmlinux.lds.cmd'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/arm/kernel/vmlinux.lds.S'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/arm/kernel/boot/Makefile'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/i386/kernel/vmlinux.lds.S'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/i386/boot/compressed/head.S'])
        except KeyError:
            pass
        try:
            print_blob(tree['Documentation/arch/x86/booting-dt.rst'])
        except KeyError:
            pass
        try:
            print_blob(tree['Documentation/arch/arm64/booting.rst'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/i386/boot/bootsect.S'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/i386/boot/setup.S'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/i386/boot/compressed/Makefile'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/arm/boot/compressed/piggy.S'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/arm/boot/compressed/vmlinux.lds.in'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/arm/boot/compressed/Makefile'])
        except KeyError:
            pass
        try:
            print_blob(tree['Documentation/arm/Booting'])
        except KeyError:
            pass
        try:
            print_blob(tree['Documentation/x86/boot.txt'])
        except KeyError:
            pass
        try:
            print_blob(tree['Documentation/arch/x86/boot.rst'])
        except KeyError:
            pass
        try:
            print_blob(tree['arch/x86/boot/boot/setup.S'])
        except KeyError:
            pass
        print_blob(tree['arch/arm/boot/compressed/head.S'])
        try:
            print_blob(tree['arch/arm/boot/compressed/vmlinux.lds.S'])
        except KeyError:
            pass
        """
        for blob in tree.blobs:
            if blob.path == 'Makefile':
                # help(blob.data_stream)
                # exit()
                # help(blob)
                # exit()
                print('=>', blob.mime_type, 'link=%s' % bool(blob.mode == blob.link_mode), '%dk' % (blob.size / 1024), blob.path, oct(blob.mode), blob.data_stream.read(96))
                break
        for tree in tree.trees:
            if tree.path == 'Documentation':
                for blob in tree.blobs:
                    if blob.path == 'Documentation/Changes':
                        print('=>', blob.mime_type, 'link=%s' % bool(blob.mode == blob.link_mode), '%dk' % (blob.size / 1024), blob.path, oct(blob.mode), blob.data_stream.read(96))
                        break
                for tree in tree.trees:
                    if tree.path == 'Documentation/process':
                        for blob in tree.blobs:
                            if blob.path == 'Documentation/process/changes.rst':
                                print('=>', blob.mime_type, 'link=%s' % bool(blob.mode == blob.link_mode), '%dk' % (blob.size / 1024), blob.path, oct(blob.mode), blob.data_stream.read(96))
                                break

                break
        """
    elif tag_object.type == 'tree':
        print(f'  [tree ref={tag_object.hexsha}]')
    print()
