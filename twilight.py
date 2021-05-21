#!/usr/bin/python3

import argparse
import configparser
import os
import subprocess

DEFAULT_STEP = 10
DEFAULT_RATE = 100

DEFAULT_PATH_CONFIG = os.path.join(os.environ['HOME'], '.twilight.conf')


class Configuration(object):

    def __init__(self, path_config, display):

        self.file = path_config
        self.rate = DEFAULT_RATE
        self.step = DEFAULT_STEP

        if display:
            self.display = display
        else:
            self.display = Configuration.get_primary_display()

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

    def lighter(self, step=0):
        if step:
            self.rate += step
        else:
            self.rate += self.step

    def darker(self, step=0):
        if step:
            self.rate += step
        else:
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
            ['xrandr', '--output', self.display, '--brightness', str(value)])

    @staticmethod
    def get_primary_display():

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
        '--display', '-d', help='Display')
    parser.add_argument(
        '--step', '-s', help='Step')
    args = parser.parse_args()

    configuration = Configuration(args.config, args.display)

    if args.value in ['mem', '-', '+']:

        # Restore previous value
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
