from bs4 import BeautifulSoup
import urllib.request
import datetime
import argparse

"""
Q.py

Genererar en textsträng med veckans lunch.
"""

def getWeeksLunchInDict():
    f = urllib.request.urlopen('http://www.hors.se/veckans-meny/')
    html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    newSoup = soup.findAll('td', { "width" : '33%' }, "html.parser")

    # Räknar med att det är bara lunch mellan Mån och Fre, tre måltider per dag

    # Värden som behöver memoreras
    week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    savedLunches = {}
    temp = []

    i = 0   # Säger vilken måltid jag är på
    k = 0   # Vilken dag jag är på
    for td in newSoup:
        temp.append(td.text)
        i += 1

        if i == 3:
            tpl = tuple(temp)
            savedLunches[week[k]] = tpl
            k += 1

            # Resettar värden
            i = 0
            temp = []

            # Hoppar ut ur loopen om jag når lördag
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

def printWeeksLunch():
    lunch = getWeeksLunchInDict()

    for i in range(5):
        wday = getSwedishWday(i)
        print(wday)
        for l in lunch[getWday(i)]:
            print(l)
            #print( '*\t' + l)

def printTodaysLunch():
    lunch = getWeeksLunchInDict()

    wd = datetime.datetime.today().weekday()
    wday_str = getSwedishWday(wd)

    print("Idag (" + wday_str + ") blir det:")
    for l in lunch[getWday(wd)]:
        print('* ' + l, end='')

def main():
	parser = argparse.ArgumentParser(description="Generate the current weeks lunch at a restaurant owned by Högskolerestauranger AB")
	parser.add_argument("--today", dest="lunches", action="store_const", const=printTodaysLunch, default=printWeeksLunch, help="Printing todays lunch. (default: this weeks lunches)")

	args = parser.parse_args()

	args.lunches()
	#printTodaysLunch()
    #printWeeksLunch()

if __name__ == "__main__":
    main()
