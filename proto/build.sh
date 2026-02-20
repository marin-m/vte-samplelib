#!/bin/bash

cd "$(dirname "$0")"
set -ex

protoc --proto_path="." --python_out="../src/vmlinux_to_elf_samplelib/pb/" \
    re/fossplant/vte_samplelib/*.proto