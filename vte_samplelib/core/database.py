#!/usr/bin/python3
# -*- encoding: Utf-8 -*-

"""
* http://synology-marin/mediawiki/index.php?title=Vmlinux-to-elf/Planned_modules/Shared_database
  * https://github.com/coleifer/peewee#readme
  * https://docs.peewee-orm.com/en/latest/peewee/quickstart.html#quickstart
  * https://docs.peewee-orm.com/en/latest/peewee/models.html
* http://synology-marin/mediawiki/index.php?title=Vmlinux-to-elf/Planned_modules/Linux_kernel_version_DB
  * https://en.wikipedia.org/wiki/Linux_kernel_version_history
    * https://www.mediawiki.org/wiki/API:REST_API/Reference/Sample_code:Get_page_source
      * https://www.mediawiki.org/wiki/API:REST_API
        * curl -s "https://en.wikipedia.org/w/rest.php/v1/page/Linux_kernel_version_history" | python3 -m json.tool | less
      * https://www.wikidata.org/wiki/Q14579#P348
        * => The data seems to be available on Wikidata, likely a better choice
  * https://www.kernel.org/pub/linux/kernel/ (use FTP for enumeration?)
    * https://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.10.tar.xz
* http://synology-marin/mediawiki/index.php?title=Vmlinux-to-elf/Samples_library/Linux_2.6.10_from_Ubuntu_5.04


WIP 2025-01-25: Define database schema here
"""

from logging import basicConfig, DEBUG, debug
from os.path import dirname, realpath, exists
from os import makedirs, environ
from enum import Enum

environ['GIT_PYTHON_TRACE'] = 'full'
basicConfig(level=DEBUG)

from peewee import (
    SqliteDatabase,
    Model,
    CompositeKey,
    Check,
    TextField,
    IntegerField,
    DateField,
    DateTimeField,
    BooleanField,
    ForeignKeyField,
)

basicConfig(level=DEBUG)

CORE_DIR = dirname(realpath(__file__))
MODULE_DIR = dirname(realpath(CORE_DIR))
ROOT_DIR = dirname(realpath(MODULE_DIR))
DB_PATH = realpath(ROOT_DIR + '/database.sqlite3')

if not exists(DB_PATH):
    debug('[i] Database file does not exist: %s, creating...' % DB_PATH)

db = SqliteDatabase(DB_PATH)


class Base(Model):
    class Meta:
        database = db
        legacy_table_names = False


# Cf. https://docs.peewee-orm.com/en/latest/peewee/models.html#field-types-table

# Maybe migrate to SQLAlchemy?
# Here are the griefs towards Peewee:
#  - No secondary tables
#  - Enum fields missing

class KernelVersion(Base):
    version_string = TextField(primary_key=True)  # Git tag
    kernel_source = TextField(
        constraints=[Check("kernel_source in ('git', 'tarball')")]
    )

    browse_url = TextField(null=True)
    download_url = TextField()
    git_commit = TextField(null=True)

    release_date = DateTimeField()

class EMachineValue(Base):
    elf_machine_int = IntegerField(index=True)
    elf_machine_str = TextField(primary_key=True)

class KnownArchitecture(Base):
    architecture_code = TextField(primary_key=True)
    has_32bit_class = BooleanField(default=False)
    has_64bit_class = BooleanField(default=False)
    has_msb_class = BooleanField(default=False)
    has_lsb_class = BooleanField(default=False)

class ArchitectureEMachineLink(Base):
    architecture = ForeignKeyField(
        KnownArchitecture, backref='e_machine_links'
    )
    e_machine = ForeignKeyField(EMachineValue, backref='arch_code_links')

    class Meta:
        primary_key = CompositeKey('architecture', 'e_machine')


class KernelSupportedArch(Base):
    release = ForeignKeyField(KernelVersion, backref='supported_archs')
    architecture = ForeignKeyField(KnownArchitecture)

    class Meta:
        primary_key = CompositeKey('release', 'architecture')


class KernelRelevantFile(Base):
    release = ForeignKeyField(KernelVersion, backref='relevant_files')

    file_name = TextField()
    # data = TextField()
    architecture_code = TextField(index=True, null=True)
    vcs_browser_url = TextField(null=True)


class KernelVersionDependency(Base):
    # Parsed from the `Documentation/Changes` kernel files:

    kernel_release = ForeignKeyField(KernelVersion, backref='dependencies')
    source_file = ForeignKeyField(KernelRelevantFile, backref='extracted_info')

    dependency_name = TextField()
    minimal_version = TextField()
    base_command = TextField(index=True)
    version_command = TextField()
    dependency_is_optional = BooleanField()

    class Meta:
        primary_key = CompositeKey('kernel_release', 'base_command')


"""
class StoredKernel(Base):

    XX
        Link to disk file
            Link to KernelRelease etc
"""


class DebianRelease(Base):
    docker_archive_name = TextField(primary_key=True)
    debian_version_name = TextField(index=True)
    debian_version_number = TextField(index=True)
    debian_release_date = DateField(index=True)


db.connect()


def flush_kernel_db():
    models = [
        KernelVersion,
        EMachineValue,
        KnownArchitecture,
        ArchitectureEMachineLink,
        KernelSupportedArch,
        KernelVersionDependency,
        KernelRelevantFile,
    ]

    db.drop_tables(models)
    db.create_tables(models)


def flush_debian_db():
    models = [
        DebianRelease,
    ]

    db.drop_tables(models)
    db.create_tables(models)
