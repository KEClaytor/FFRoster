# Use Beautiful soup to get the latest police blotter
# We want to exclude these players from our roster
# This largely works, it gives some bad link names;
#  'a person' and '& rumors' are my favorites
#  but by and large it does what it needs to

from bs4 import BeautifulSoup
import urllib2
import pickle

# Extracts out the player name assuming the format;
# TEAM POSITION FIRSTNAME LASTNAME
def getNameFromText(text):
    ts = text.split()
    rv = ('','None')
    if len(ts) >= 4:
        pos = ts[-3]
        name = ts[-2] + ' ' + ts[-1]
        rv = (pos,name)
    return rv

def getPoliceBlotter():
    # Excellent police blotter site Jon found, we'll use it
    url_list=["http://profootballtalk.nbcsports.com/police-blotter/", \
        "http://profootballtalk.nbcsports.com/2009/02/08/turd-watch-ii-final-police-blotter/"]

    offenders = []
    for url in url_list:
        page=urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        for link in soup("a"):
            lt = link.get_text()
            (pos,name) = getNameFromText(lt)
            if name != 'None':
                offenders.append(name)

    # Debugging:
    #for pname in offenders:
    #    print pname
    return offenders

if __name__ == "__main__":
    f = open('policeblotter.pk','w+')
    offenders = getPoliceBlotter()
    pickle.dump(offenders,f)
    f.close()
