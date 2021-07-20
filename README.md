# Twilight

## What is twilight ?

Twilight is a brightness manager for OLED displays written in Python 3.

This is a simple helper for calling _xrandr_.

## Usage

Set the screen brightness to 60 %

$ ./twilight.py 60

Increase the brightness by 10%

$ ./twilight.py +10

Decrease the brightness by 5%

$ ./twilight.py -5

Set the brightness to last used value

$ ./twilight.py mem

## Installation

Just copy the script twilight.py anywhere you want, make it executable if needed and enjoy !

## Desktop configuration

Twilight is designed to be invisible in everyday life:
* Add __twilight.py mem__ to your desktop startup configuration and the brightness will be set to the last used value
* Link the brightness buttons of your keyboard to __twilight.py -10__ and __twilight.py +10__ to simply adujst the screen brightness
