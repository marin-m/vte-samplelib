#!/usr/bin/env python3
# -*- encoding: Utf-8 -*-
from os.path import realpath, dirname, join
from tomllib import load
from typing import Dict
from json import dumps

SCRIPT_DIR = dirname(realpath(__file__))
MODULE_DIR = dirname(realpath(SCRIPT_DIR))

BASE_DIR = dirname(realpath(MODULE_DIR))

CONFIG_PATH = join(BASE_DIR, 'config.toml')

# WIP 2025-11-30


class ConfigLoader:
    config_dict: Dict[str, object]

    def __init__(self):

        with open(CONFIG_PATH, 'rb') as fd:
            self.config_dict = load(fd)
