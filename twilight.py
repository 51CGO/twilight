#!/usr/bin/python3

import argparse
import configparser
import os
import subprocess

DEFAULT_STEP = 10
DEFAULT_RATE = 100

DEFAULT_PATH_CONFIG = os.path.join(os.environ['HOME'], '.twilight.conf')


class Configuration(object):

    def __init__(self, path_config):
        self.file = path_config
        self.rate = DEFAULT_RATE
        self.step = DEFAULT_STEP

    def load(self, path_config=None):

        if not path_config:
            path_config = self.file

        if not os.path.isfile(path_config):
            return -1

        c = configparser.ConfigParser()
        c.read(path_config)
        self.rate = c.getint('Brightness', 'Last')

    def save(self, path_config=None):

        if not path_config:
            path_config = self.file

        dir_cache = os.path.dirname(path_config)
        if not os.path.isdir(dir_cache):
            os.makedirs(dir_cache)

        fd = open(path_config, 'w')
        c = configparser.ConfigParser()
        c.add_section('Brightness')
        c.set('Brightness', 'Last', str(self.rate))
        c.write(fd)
        fd.close()

    def lighter(self):
        self.rate += self.step

    def darker(self):
        self.rate -= self.step

    def set(self, rate_new):
        self.rate = rate_new

    def fix(self):
        if self.rate > 100:
            self.rate = 100

        elif self.rate < 0:
            self.rate = 0

    def apply(self):

        value = 0.01 * self.rate
        subprocess.call(
            ['xrandr', '--output', 'eDP-1', '--brightness', str(value)])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('value')
    parser.add_argument(
        '--config', '-c', default=DEFAULT_PATH_CONFIG,
        help='Configuration file')
    parser.add_argument(
        '--display', '-d', help='Display')
    args = parser.parse_args()

    print(args.config)

    configuration = Configuration(args.config)

    if args.value in ['mem', '-', '+']:

        # restore previous value
        configuration.load()

        if args.value == '+':
            configuration.lighter()

        elif args.value == '-':
            configuration.darker()

    elif args.value.isdigit():
        configuration.set(int(args.value))

    else:
        exit(1)

    configuration.fix()
    configuration.apply()
    configuration.save()
