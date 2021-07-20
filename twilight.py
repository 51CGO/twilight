#!/usr/bin/python3

import argparse
import configparser
import os
import subprocess

DEFAULT_RATE = 100

DEFAULT_PATH_CONFIG = os.path.join(os.environ['HOME'], '.twilight.conf')


def load(path_config):

    c = configparser.ConfigParser()
    c.read(path_config)
    return c.getint('Brightness', 'Last')


def save(path_config, value):

    dir_cache = os.path.dirname(path_config)
    if not os.path.isdir(dir_cache):
        os.makedirs(dir_cache)

    fd = open(path_config, 'w')
    c = configparser.ConfigParser()
    c.add_section('Brightness')
    c.set('Brightness', 'Last', str(value))
    c.write(fd)
    fd.close()

def set(value):

    val = 0.01 * value
    display = get_display()
    subprocess.call(
        ['xrandr', '--output', display, '--brightness', str(val)])

def get_display():

    display = None

    xrandr = subprocess.Popen(
        'xrandr', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = xrandr.communicate()
    for line in out.splitlines():

        if line.count(b"connected primary"):

            items = line.split()
            display = items[0]
            break

    return display


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('value')
    parser.add_argument(
        '--config', '-c', default=DEFAULT_PATH_CONFIG,
        help='Configuration file')
    parser.add_argument(
        '--force', '-f', action="store_true",
        help='Force application of exotic values')
    args = parser.parse_args()

    value = None

    if args.value == 'mem':
        value = load(args.config)

    elif args.value[0] == "+":

        if args.value[1:].isdigit():
            value = load(args.config)
            value += int(args.value[1:])

    elif args.value[0] == "-":

        if args.value[1:].isdigit():
            value = load(args.config)
            value -= int(args.value[1:])

    elif args.value.isdigit():
        value = int(args.value)

    if not value:
        exit(1)

    if not args.force:

        if value > 100:
            value = 100

    if value < 0:
        value = 0

    set(value)
    save(args.config, value)
