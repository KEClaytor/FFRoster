# This script pulls data looking at player, position, and ff score
#  Data for player scoring is pulled from fftoday.com/stats
#  Data for estimated player cost is pulled from http://www.fftoolbox.com/ and from http://espn.go.com/
# We save this data to text files and then parse those, as my BS4 isn't good enough to pull from web yet

from PlayerStorage import PlayerStorage
import pickle

def mergePointsAndCost(points,costa,costb):
    merged = PlayerStorage()
    for name in points.names:
        (na,pa,pta,ca) = costa.getplayer(name)
        (nb,pb,ptb,cb) = costa.getplayer(name)
        (n,p,pt,c) = points.getplayer(name)
        merged.addplayer(name,pos=p,points=pt,cost=(ca+cb)/2)
    return merged

def makePlayerList():
    # Parse the EPSN cost data
    cost_espn = PlayerStorage()
    fnames = open('costESPN.dat')
    for line in fnames:
        lv = line.strip().split('\t')
        nv = lv[1].split()
        nv.pop()
        name = ' '.join(nv).strip(', ')
        mc = lv[4].strip()
        if mc != '--':
            cost = int(mc[1::])
        else:
            cost = 0
        cost_espn.addplayer(name,cost=cost)

    # Parse the fftoolbox.com cost data
    cost_ff = PlayerStorage()
    fnames = open('costFF.dat')
    for line in fnames:
        lv = line.strip().split('\t')
        name = lv[1]
        mc = lv[-1]
        cost = int(mc[1::])
        cost_ff.addplayer(name,cost=cost)

    # Parse the scoring data from fftoday.com
    points = PlayerStorage()
    positions = ['QB','RB','WR','TE','K','DEF']
    for pos in positions:
        fname = 'pts' + pos + '.dat'
        fnames = open(fname)
        for line in fnames:
            lv = line.strip().split('\t')
            nv = lv[0].split()
            nv.pop(0)
            name = ' '.join(nv).strip() # get rid of the last space
            pts = float(lv[-2])
            points.addplayer(name,pos=pos,points=pts)
    
    return (points,cost_espn,cost_ff)

if __name__ == "__main__":
    # Get the points and cost values for our players
    (points,cost_espn,cost_ff) = makePlayerList()
    # Debugging:
    cost_espn.listplayers()
    cost_ff.listplayers()
    points.listplayers()
    # Merge these into one vector of (name,pos,points,cost)
    players = mergePointsAndCost(points,cost_espn,cost_ff)
    players.listplayers()

    # Pickle and dump
    f = open('playerstats.pk','w+')
    pickle.dump(players,f)
    f.close()

