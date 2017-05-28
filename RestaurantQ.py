from bs4 import BeautifulSoup
import urllib.request
import datetime
import argparse
import arrow

"""
RestaurantQ.py
--------------
A program that shows what lunches are available on Restaurant Q.

Copyright 2017 Olof Sjödin <me@olofsjodin.se>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

def lunchTimeOverToday():
    closingTime = 14
    nowTime = arrow.utcnow().to("Europe/Stockholm").hour

    return True if closingTime < nowTime else False

def getNextWeekDateStr():
    now = arrow.utcnow()
    return now.replace(weeks=+1).format('YYYY-MM-DD')

def getWeeksLunchInDict(english=True, showNextWeek=False):
    url = ""
    if showNextWeek:
        nextWeek = getNextWeekDateStr()
        url = 'http://www.hors.se/veckans-meny/?week_for=' + nextWeek

        if english:
            url += '&l=e'
    else:
        url = 'http://www.hors.se/veckans-meny/'

        if english:
            url += '?l=e'


    f = urllib.request.urlopen(url)
    html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    newSoup = soup.findAll('td', { "width" : '33%' }, "html.parser")

    week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    savedLunches = {}
    temp = []

    i = 0
    k = 0
    for td in newSoup:
        temp.append(td.text)
        i += 1

        if i == 3:
            tpl = tuple(temp)
            savedLunches[week[k]] = tpl
            k += 1

            i = 0
            temp = []

            if k == 5:
                return savedLunches

def getEnglishWday(n):
	week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	return week[n]

def getSwedishWday(n):
    week = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"]
    return week[n]

def getWday(n):
    week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    return week[n]

def todayWdayNr():
    ret = datetime.datetime.today().weekday()
    return ret

def printWeeksLunch(english=True, showPastLunches=False):
    lunch = getWeeksLunchInDict(english=english)

    todayNr = todayWdayNr()

    if lunchTimeOverToday():
        todayNr += 1

    if not showPastLunches:
        todayNr = 0

    if todayNr < 5:
        for i in range(todayNr, 5):
            wday = getSwedishWday(i) if not english else getEnglishWday(i)

            print(wday + ":")
            for l in lunch[getWday(i)]:
                print("* " + l)
                #print( '*\t' + l)
    else:
        lunch = getWeeksLunchInDict(english=english, showNextWeek=True)
        for i in range(0, 5):
            wday = getSwedishWday(i) if not english else getEnglishWday(i)

            print(wday + ":")
            for l in lunch[getWday(i)]:
                print("* " + l, end="")
                #print( '*\t' + l)

def printTodaysLunch(english=True):
    wd = todayWdayNr()

    if lunchTimeOverToday():
        wd += 1

    showNextWeek = False
    if wd > 4:
        showNextWeek = True
        wd = 0

    lunch = getWeeksLunchInDict(english=english, showNextWeek=showNextWeek)


    wday = getSwedishWday(wd) if not english else getEnglishWday(wd)

    print("" + wday + ":")
    for l in lunch[getWday(wd)]:
        print('* ' + l, end='')

def main():
    parser = argparse.ArgumentParser(description="Generate the current weeks lunch at a restaurant owned by Högskolerestauranger AB")
    #parser.add_argument("--today", dest="lunches", action="store_const", const=printTodaysLunch, default=printWeeksLunch, help="Printing todays lunch. (default: this weeks lunches)")
    parser.add_argument("--today", dest="showTodayOnly", action="store_true")
    parser.add_argument("--swedish", dest="translateToSwedish", action="store_false")
    parser.add_argument("--show-past-lunches", dest="showPastLunches", action="store_false")
    args = parser.parse_args()

    # Will translate to Swedish if the flag is set i.e. if the variable is False
    #args.lunches(english=args.translateToSwedish, showPastLunches=args.showPastLunches)
    if args.showTodayOnly:
        printTodaysLunch(english=args.translateToSwedish)
    else:
        printWeeksLunch(english=args.translateToSwedish, showPastLunches=args.showPastLunches)
    #printTodaysLunch()
    #printWeeksLunch()

if __name__ == "__main__":
    main()
