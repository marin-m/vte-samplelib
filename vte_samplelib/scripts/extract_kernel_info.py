# xx NEXT WIP 2026-02-20

from vte_samplelib.core.config_loader import ConfigLoader

from vte_samplelib.core.database import (
    KernelVersion,
    KernelVersionDependency,
    KernelRelevantFile,
    flush_kernel_db,
)

from git import Repo, Blob
from logging import info

from vte_samplelib.version_management.git_extractor import (
    ExtraGitParser,
    ChangelogParser,
)

REMOTE_URL = (
    'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/'
)
TREE_ROOT_URL = REMOTE_URL + 'tree/?id=%s'
SNAPSHOT_URL = REMOTE_URL + 'snapshot/%s.tar.gz'


def main():
    flush_kernel_db()

    config = ConfigLoader().config_dict

    repo = Repo(config['kernel-tree']['git-dir'])

    seen_refs: set[str] = set()
    seen_archs: set[str] = set()
    seen_e_machines: set[str] = set()

    for tag_ref in repo.tags:
        tag = tag_ref.object
        tag_object = tag.object

        if tag.tag in seen_refs:
            continue
        seen_refs.add(tag.tag)

        if tag_object.type == 'commit':
            tree = tag_object.tree

            info('Writing info for %s to DB' % tag.tag)

            kernel = KernelVersion()
            kernel.version_string = tag.tag
            kernel.kernel_source = 'git'
            kernel.browse_url = TREE_ROOT_URL % tag.tag
            kernel.download_url = SNAPSHOT_URL % tag.tag
            kernel.git_commit = tag_object.hexsha
            kernel.release_date = tag_object.committed_datetime
            kernel.save(force_insert=True)

            for arch_dir in tree['arch'].trees:
                arch_code = arch_dir.name
                if arch_code != 'um':
                    ExtraGitParser(
                        tree,
                        kernel,
                        arch_code,
                        arch_code in seen_archs,
                        seen_e_machines,
                    )
                    seen_archs.add(arch_code)

            ChangelogParser(tree, kernel)
