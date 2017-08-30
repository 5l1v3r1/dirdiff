#!/usr/bin/env python3

# dirdiff -- Compare two directories, print file names with difference
# Copyright (C) 2017  StarBrilliant <13253@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys


def walk_on_error(error):
    raise error


def compare_file(nameA, nameB):
    try:
        fileA = open(nameA, 'rb')
    except FileNotFoundError:
        return False
    try:
        fileB = open(nameB, 'rb')
    except FileNotFoundError:
        fileA.close()
        return False
    while True:
        chunkA = fileA.read(4096)
        chunkB = fileB.read(4096)
        if chunkA == chunkB:
            if len(chunkA) == 0:
                fileB.close()
                fileA.close()
                return True
        else:
            fileB.close()
            fileA.close()
            return False


def main(argv):
    if len(argv) != 4:
        print('Usage: {} oldDir newDir output'.format(argv[0]))
        print()
        return
    oldDir = argv[1]
    newDir = argv[2]
    output = argv[3]
    outputFile = open(output, 'w', encoding='utf-8')
    files = set()
    for dirpath, dirnames, filenames in os.walk(oldDir):
        sys.stderr.write('Scan: {}\n'.format(dirpath))
        for name in filenames:
            files.add(os.path.relpath(os.path.join(dirpath, name), oldDir))
    for dirpath, dirnames, filenames in os.walk(newDir):
        sys.stderr.write('Scan: {}\n'.format(dirpath))
        for name in filenames:
            files.add(os.path.relpath(os.path.join(dirpath, name), newDir))
    files = list(files)
    files.sort()
    for name in files:
        if compare_file(os.path.join(oldDir, name), os.path.join(newDir, name)):
            sys.stderr.write('Same: {}\n'.format(name))
        else:
            sys.stderr.write('Diff: {}\n'.format(name))
            outputFile.write(name + '\n')
    outputFile.close()


if __name__ == '__main__':
    main(sys.argv)
