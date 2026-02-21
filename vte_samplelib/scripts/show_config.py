#!/usr/bin/env python3
# -*- encoding: Utf-8 -*-
from vte_samplelib.core.config_loader import ConfigLoader
from json import dumps


def main():
    loader = ConfigLoader()

    print(dumps(loader.config_dict, indent=4))


if __name__ == "__main__":
    main()
