#!/usr/bin/python3

import argparse
import configparser
import os
import subprocess

DEFAULT_STEP = 10

FILE_CACHE = os.path.join(os.environ['HOME'], '.cache', 'twilight')


def check_value(rate):
    if rate > 100 or rate < 10:
        return False
    return True


def load():

    if not os.path.isfile(FILE_CACHE):
        return -1

    c = configparser.ConfigParser()
    c.read(FILE_CACHE)
    rate = c.getint('Brightness', 'Last')

    return rate


def save(rate):

    dir_cache = os.path.dirname(FILE_CACHE)
    if not os.path.isdir(dir_cache):
        os.makedirs(dir_cache)

    with open(FILE_CACHE, 'w') as fd:
        c = configparser.ConfigParser()
        c.add_section('Brightness')
        c.set('Brightness', 'Last', str(rate))
        c.write(fd)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('value')
    parser.add_argument('--cache', default=FILE_CACHE, help='Cache file')
    args = parser.parse_args()

    if args.value in ['mem', '-', '+']:

        # restore previous value
        rate = load()

        if args.value == '+':
            rate += DEFAULT_STEP

        elif args.value == '-':
            rate -= DEFAULT_STEP

    elif args.value.isdigit():
        rate = int(args.value)

    else:
        exit(1)

    if rate > 100:
        rate = 100

    if rate < 10:
        rate = 10

    value = 0.01 * rate

    subprocess.call(
        ['xrandr', '--output', 'eDP-1', '--brightness', str(value)])

    save(rate)
