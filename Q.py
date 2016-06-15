from bs4 import BeautifulSoup
import urllib.request

"""
Q.py

Genererar en textsträng med vekans lunch.
"""

def getWeeksLunchInDict():
    f = urllib.request.urlopen('http://www.hors.se/veckans-meny/?rest=171')
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

def printWeeksLunch():
    lunch = getWeeksLunchInDict()

    week = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]

    for wd in week:
        print(wd)
        for l in lunch[wd]:
            print( '*\t' + l)

def main():
    printWeeksLunch()

if __name__ == "__main__":
    main()
