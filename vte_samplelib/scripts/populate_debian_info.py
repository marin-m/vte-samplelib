#!/usr/bin/env python3
# -*- encoding: Utf-8 -*-

from datetime import date

from vte_samplelib.core.database import (
    DebianRelease,
    flush_debian_db,
)

"""
    WIP
        ==> https://www.debian.org/releases/

        GOAL: Use Docker Hub API (or just a static
          list for the moment) to list available
          images and suggest them through the
          vmlinux-to-elf CLI/GUI?

        https://hub.docker.com/r/debian/eol/
        => Buzz - 1.1 - debian/eol:buzz - 17/06/1996
        => Rex - 1.2 - debian/eol:rex - 12/12/1996
        => Bo - 1.3 - debian/eol:bo - 02/07/1997
        => Hamm - 2.0 - debian/eol:hamm - 24/07/1997
        => Slink - 2.1 - debian/eol:slink -24/07/1998
        => Potato - 2.2 - debian/eol:potato - 15/08/2000
        => Woody - 3.0 - debian/eol:woody - 19/07/2002
        => Sarge - 3.1 - debian/eol:sarge - 06/06/2005
        => Etch - 4.0 - debian/eol:etch - 08/04/2007
        => Lenny - 5.0 - debian/eol:lenny - 14/02/2009
        => Squeeze - 6.0 - debian/eol:squeeze - 06/02/2011
        => Wheezy - 7.0 - debian/eol:wheezy - 04/05/2013
        => Jessie - 8.0 - debian/eol:jessie - 25/04/2015
        => Stretch - 9.0 - debian/eol:stretch - 17/06/2017
        => Buster - 10.0 - debian/eol:buster - 06/07/2019
        => Bullseye - 11.0 - debian/eol:bullseye - 14/08/2021

            - https://docs.docker.com/reference/api/hub/latest/#tag/resources
                - https://docs.docker.com/reference/api/hub/latest/#tag/repositories

        https://hub.docker.com/r/debian/snapshot
            => debian/snapshot:buster-20180716
            => debian/snapshot:jessie-20180716
            => etc.
        https://hub.docker.com/_/debian/
            => Bookworm - 12.0 - debian:bookworm / https://hub.docker.com/_/debian/tags?name=bookworm - 12.0 - 10/06/2023
            => Trixie - 13.0 - debian:trixie / https://hub.docker.com/_/debian/tags?name=trixie - 09/08/2025
        Use a static table?
        https://en.wikipedia.org/wiki/Debian_release_version_history
        https://fr.wikipedia.org/wiki/Historique_des_versions_de_Debian

"""

def main():

    flush_debian_db()
    populate_debian_versions_static()

def populate_debian_versions_static():

    for (
        debian_version_name,
        debian_version_number,
        docker_archive_name,
        debian_release_date,
    ) in [
        ('Buzz', '1.1', 'debian/eol:buzz', date(1996, 6, 17)),
        ('Rex', '1.2', 'debian/eol:rex', date(1996, 12, 12)),
        ('Bo', '1.3', 'debian/eol:bo', date(1997, 7, 2)),
        ('Hamm', '2.0', 'debian/eol:hamm', date(1997, 7, 24)),
        ('Slink', '2.1', 'debian/eol:slink', date(1998, 7, 24)),
        ('Potato', '2.2', 'debian/eol:potato', date(2000, 8, 15)),
        ('Woody', '3.0', 'debian/eol:woody', date(2002, 7, 19)),
        ('Sarge', '3.1', 'debian/eol:sarge', date(2005, 6, 6)),
        ('Etch', '4.0', 'debian/eol:etch', date(2007, 4, 8)),
        ('Lenny', '5.0', 'debian/eol:lenny', date(2009, 2, 14)),
        ('Squeeze', '6.0', 'debian/eol:squeeze', date(2011, 2, 6)),
        ('Wheezy', '7.0', 'debian/eol:wheezy', date(2013, 5, 4)),
        ('Jessie', '8.0', 'debian/eol:jessie', date(2015, 4, 25)),
        ('Stretch', '9.0', 'debian/eol:stretch', date(2017, 6, 17)),
        ('Buster', '10.0', 'debian/eol:buster', date(2019, 7, 6)),
        ('Bullseye', '11.0', 'debian/eol:bullseye', date(2021, 8, 14)),
        ('Bookworm', '12.0', 'debian/bookworm', date(2023, 6, 10)),
        ('Trixie', '13.0', 'debian/trixie', date(2025, 8, 9)),
    ]:
        release = DebianRelease()
        release.debian_version_name = debian_version_name
        release.debian_version_number = debian_version_number
        release.docker_archive_name = docker_archive_name
        release.debian_release_date = debian_release_date
        release.save(force_insert=True)
