from bs4 import BeautifulSoup
import urllib.request
import datetime
import argparse
import arrow
import json
import os.path
import os

"""
RestaurantQ.py
--------------
A program that shows what lunches are available on Restaurant Q.

Copyright 2018 Olof Sjödin <me@olofsjodin.se>

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
    if existenceOfCache():
        return loadCache()        
    else:
        return updateCacheAndReturnLunches(english, showNextWeek)

def updateCacheAndReturnLunches(english=True, showNextWeek=False):
    url = 'http://www.hors.se/veckans-meny/?rest=171'
    if showNextWeek:
        nextWeek = getNextWeekDateStr()
        url += '&week_for=' + nextWeek
    if english:
        url += '&l=e'

    lunch = downloadLunchesToDict(url)
    saveToCache(lunch)
    return lunch
    

def downloadLunchesToDict(url):
    f = urllib.request.urlopen(url)
    html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    foodtable = soup.select("#mattabellen")
    foodtable = foodtable[0]

    ret = {}
    week_index = 0
    for tr in foodtable.findAll('tr')[1:]:
        temp = []
        for td in tr.findAll('td'):
            if td.text != "":
                temp.append(td.text)
        ret[getWday(week_index)] = tuple(temp)
        week_index += 1
    return ret
    

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
        print('* ' + l)

# Cache management

CACHE_LOC = os.getenv("HOME") + "/.cache/restaurant_q.tmp"

def saveToCache(lunch):
    cacheCont = {}
    nextWeekDl = 5-todayWdayNr()
    cacheCont["next_dl"] = str(datetime.date.today() + datetime.timedelta(days=nextWeekDl))
    cacheCont["lunches"] = lunch
    
    with open(CACHE_LOC, 'w+') as outfile:
        json.dump(cacheCont, outfile)

def loadCache():
    with open(CACHE_LOC, "r") as o:        
        cache = json.loads(o.read())
        
        # Update cache if it is due
        dueDate = datetime.datetime.strptime(cache['next_dl'], '%Y-%m-%d')
        if datetime.datetime.today() >= dueDate:
            return updateCacheAndReturnLunches()
        else:
            return cache["lunches"]

def existenceOfCache():
    return os.path.isfile(CACHE_LOC)
    

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

