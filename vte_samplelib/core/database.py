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

from peewee import SqliteDatabase, Model, TextField, DateField, ForeignKeyField

CORE_DIR = dirname(realpath(__file__))
ROOT_DIR = dirname(dirname(dirname(CORE_DIR)))
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

class KernelRelease(Base):

    version_string = TextField()
    release_date = DateField()

    # Xx Dependencies table here (parse Changelog.txt?)
    #     => Link to n KernelReleaseDependency

    git_tag = TextField() # optional, or just tarball URL if not available
    tarball_url = TextField()
    vcs_browser_url = TextField() # optional, or just tarball URL if not available

class KernelReleaseDependency(Base):
    
    # Parsed from the `Documentation/Changes` kernel files:

    release = ForeignKeyField(KernelRelease, backref = 'dependencies')

    dependency_name = TextField()
    minimal_version = TextField()
    version_check_cmd = TextField()
    base_cmd = TextField()

"""
class KernelReleaseKallsymsRelatedFile(Base):
    xx
    file_name
    commit_hash
    commit_desc
    vcs_browser_url

class StoredKernel(Base):

    XX
        Link to disk file
            Link to KernelRelease etc

class DebianRelease(Base):

    XX
"""

# db.connect()
# db.create_tables([KernelRelease, KernelReleaseDependency])
