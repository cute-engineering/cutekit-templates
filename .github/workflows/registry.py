#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys


def addEntry(entry: str) -> dict:
    with open(os.path.join(entry, 'project.json'), 'r') as f:
        project: dict = json.load(f)

    return {
        'id': os.path.basename(project['id']),
        'description': project['description']
    }


def main() -> None:
    registry = []

    if os.path.basename(os.getcwd()) != 'cutekit-template':
        print("Please run this on the root of the repository", file=sys.stderr)
        exit(1)

    for entry in os.listdir('.'):
        if os.path.isdir(entry) and os.path.isfile(os.path.join(entry, 'project.json')):
            registry.append(addEntry(entry))

    with open('registry.json', 'w') as f:
        json.dump(registry, f)


if __name__ == '__main__':
    main()