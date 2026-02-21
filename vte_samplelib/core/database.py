#!/usr/bin/python3
#-*- encoding: Utf-8 -*-

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

from os.path import dirname, realpath, exists
from logging import debug, getLogger, DEBUG
from os import makedirs
from enum import Enum

from peewee import (SqliteDatabase, Model, TextField,
                    DateTimeField, BooleanField, ForeignKeyField)
from peewee_enum_field import EnumField

CORE_DIR = dirname(realpath(__file__))
MODULE_DIR = dirname(realpath(CORE_DIR))
ROOT_DIR = dirname(realpath(MODULE_DIR))
DB_PATH = realpath(ROOT_DIR + '/database.sqlite3')

logger = getLogger()
logger.setLevel(DEBUG)

# TODO: Write basic scrapers before implementing the database?

if not exists(DB_PATH):

    debug('[i] Database file does not exist: %s, creating...' % DB_PATH)

db = SqliteDatabase(DB_PATH)

class Base(Model):
    class Meta:
        database = db
        legacy_table_names = False

class KernelSource(Enum):
    SOURCE_GIT = 1
    SOURCE_TARBALL = 2

# Cf. https://docs.peewee-orm.com/en/latest/peewee/models.html#field-types-table

class KernelVersion(Base):

    # "Because we have not specified a primary key, peewee will
    # automatically add an auto-incrementing integer primary
    # key field named id.

    version_string = TextField() # Git tag
    kernel_source = EnumField(KernelSource)

    browse_url = TextField()
    download_url = TextField()
    git_commit = TextField()

    release_date = DateTimeField()

    # Xx Dependencies table here (parse Changelog.txt?)
    #     => Link to n KernelReleaseDependency

class KernelVersionDependency(Base):
    
    # Parsed from the `Documentation/Changes` kernel files:

    release = ForeignKeyField(KernelVersion, backref = 'dependencies')

    dependency_name = TextField()
    minimal_version = TextField()
    base_command = TextField()
    version_command = TextField()
    dependency_is_optional = BooleanField()

class KernelRelevantFile(Base):
    release = ForeignKeyField(KernelVersion, backref = 'relevant_files')

    file_name = TextField()
    data = TextField()
    architecture_code = TextField(index = True)
    vcs_browser_url = TextField()

"""
class StoredKernel(Base):

    XX
        Link to disk file
            Link to KernelRelease etc

class DebianRelease(Base):

    XX
"""

db.connect()

def flush_kernel_db():
    models = [
        KernelVersion,
        KernelVersionDependency,
        KernelRelevantFile
    ]
    
    db.drop_tables(models)
    db.create_tables(models)
