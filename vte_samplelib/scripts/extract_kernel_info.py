# xx NEXT WIP 2026-02-20

vte_samplelib.core.config_loader import

from vte_samplelib.core.database import (
    KernelVersion,
    KernelSource,
    KernelVersionDependency,
    KernelRelevantFile,
    flush_kernel_db
)

from git import Repo, Blob

from vte_samplelib.version_management.git_extractor import (
    GitParser,
    ChangelogParser
)

def main():
    flush_kernel_db()

    git = Repo(xx)

    kernel = KernelVersion(xx = xx)
    kernel.save()
    exit('TODO')