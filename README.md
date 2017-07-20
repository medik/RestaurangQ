# RestaurantQ

## What is this?
This is a program that goes into [the current menu ](http://www.hors.se/veckans-meny/) at the local restaurant located in [Q at KTH](https://www.google.se/maps/place/Restaurang+Q/@59.3502264,18.0655218,17z/data=!3m1!4b1!4m5!3m4!1s0x465f9d14cd33f4db:0xc3214c8075600bd!8m2!3d59.3502264!4d18.0677105). But works also for every other restaurant owned by the same company.

## How do I use it?
Run the following commands:
```
$ git clone https://github.com/medik/RestaurantQ.git
$ cd RestaurantQ
$ pip3 install arrow bs4
$ python3 RestaurantQ.py -h
usage: RestaurantQ.py [-h] [--today] [--swedish] [--show-past-lunches]

Generate the current weeks lunch at a restaurant owned by Högskolerestauranger
AB

optional arguments:
  -h, --help           show this help message and exit
  --today
  --swedish
  --show-past-lunches
```

By adding the help flag, i.e. `-h`, you can see what available commands you can use. Personally, I use this program together with GeekTools to view this week's lunch menu on my desktop. The result is shown here:

![screenshot](http://i.imgur.com/N19v7h3.jpg)

## Legal
This script is protected under GNU General Public License 3.0, see the COPYING file for more information.

