from bs4 import BeautifulSoup
import urllib.request
import datetime

"""
Q.py

Genererar en textsträng med vekans lunch.
"""

def getWeeksLunchInDict():
    f = urllib.request.urlopen('http://www.hors.se/veckans-meny/')
    html = f.read()

    soup = BeautifulSoup(html, "lxml")
    newSoup = soup.findAll('td', { "width" : '33%' }, "lxml")

    # Räknar med att det är bara lunch mellan Mån och Fre, tre måltider per dag

    # Värden som behöver memoreras
    week = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]
    savedLunches = {}
    temp = []

    i = 0   # Säger vilken måltid jag är på
    k = 0   # Vilken dag jag är på
    for td in newSoup:
        temp.append(td.string)
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

def getSwedishWday(n):
    week = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"]
    return week[n]

def printWeeksLunch():
    lunch = getWeeksLunchInDict()

    week = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]

    for wd in week:
        print(wd)
        for l in lunch[wd]:
            print(l)
            #print( '*\t' + l)

def printTodaysLunch():
    lunch = getWeeksLunchInDict()

    wd = datetime.datetime.today().weekday()
    wday_str = getSwedishWday(wd)

    print("Idag (" + wday_str + ") blir det:")
    for l in lunch[wday_str]:
        print('* ' + l)

def main():
    printTodaysLunch()

if __name__ == "__main__":
    main()
