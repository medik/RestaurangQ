from bs4 import BeautifulSoup
import urllib.request
import datetime
import argparse

"""
RestaurantQ.py

Generate the current weeks lunch at a restaurant owned by Högskolerestauranger AB
"""

def getWeeksLunchInDict(english=True):
    f = urllib.request.urlopen('http://www.hors.se/veckans-meny/')

    if english:
        f = urllib.request.urlopen('http://www.hors.se/veckans-meny/?l=e')

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

def printWeeksLunch(english=True):
    lunch = getWeeksLunchInDict(english=english)

    for i in range(5):
        wday = getSwedishWday(i) if not english else getEnglishWday(i)

        print(wday + ":")
        for l in lunch[getWday(i)]:
            print("* " + l, end="")
            #print( '*\t' + l)

def printTodaysLunch(english=True):
    lunch = getWeeksLunchInDict(english=english)

    wd = datetime.datetime.today().weekday()
    wday = getSwedishWday(wd) if not english else getEnglishWday(wd)

    print("" + wday + ":")
    for l in lunch[getWday(wd)]:
        print('* ' + l, end='')

def main():
    parser = argparse.ArgumentParser(description="Generate the current weeks lunch at a restaurant owned by Högskolerestauranger AB")
    parser.add_argument("--today", dest="lunches", action="store_const", const=printTodaysLunch, default=printWeeksLunch, help="Printing todays lunch. (default: this weeks lunches)")
    parser.add_argument("--swedish", dest="translateToSwedish", action="store_false")
    args = parser.parse_args()

    # Will translate to Swedish if the flag is set i.e. if the variable is False
    args.lunches(english=args.translateToSwedish)
    #printTodaysLunch()
    #printWeeksLunch()

if __name__ == "__main__":
    main()
