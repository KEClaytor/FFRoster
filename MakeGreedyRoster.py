# The heavy-lifter program
# This makes our roster using a greedy algorithm for knapsack pakcing
#  Essentially we're maximizing our team value while minimizing cost
#  We also have some constraints like limited QB's, etc.
#  The greedy algorithm doesn't particularlly handle these all too well
#  but it should get us close enough

from PlayerStorage import PlayerStorage
import copy
import pickle

# Returns True of the roster is filled, False otherwise
def rfilled(nteam):
    rt = False
    spots = 0
    for x in nteam:
        spots += nteam[x]
    if spots == 0:
        rt = True
    return rt

def listPurchased(players,mycash,teampoints):
    for idx in range(len(players)):
        (name,pos,points,cost) = players.getplayer(idx)
        teampoints += players.points[idx]
        mycash -= cost
        print "Purchase %20s to fill %3s for %4d\tTeam worth: %5.2f\tRemaining cash $%d" % (name,pos,cost,teampoints,mycash)
    return

def optimizeRoster(players,budget,nteam):
    cashleft = budget
    wfac = 1
    # Keep going until we just run out of cash
    # As players get picked the weighting factor will increase
    # This decreases the relative weights of the leftover players
    while (cashleft > 0):
        print "Optimizing team: $%d left with weight %d." % (cashleft,wfac)
        weight = players.getweight(wfac)
        (purchase,cashleft) = makeRoster(copy.deepcopy(players),weight,budget,copy.deepcopy(nteam))
        # Increase the weighting factor if that wasn't enough
        wfac += 1
    return purchase

# Generate the best roster we can from a playerlist
#  without going over-budget
def makeRoster(players,weights,budget,nteam):
    purchased = PlayerStorage()
    # Now try to maximize our team value
    while not rfilled(nteam):
        # Duplicate players and weights
        playerscopy = players.copy()
        weightscopy = copy.deepcopy(weights)
        filled = False
        while (not filled):
            try:
                maxw = max(weightscopy)
            except ValueError:
                print "Whoops, check weights length"
            idx = weightscopy.index(maxw)
            pos = playerscopy.pos[idx]
            #print "Searching for %s which has %d remaining slots." % (pos, nteam[pos])
            # We found a valid player
            if nteam[pos] > 0:
                nteam[pos] = nteam[pos]-1
                filled = True
            else:
                weightscopy.pop(idx)
                playerscopy.removeplayer(idx)
        # We have found a player, append them to our purchased list
        #  and remove from the non-copy players list
        # Note: the player idx came from the copylist
        (name,pos,points,cost) = playerscopy.getplayer(idx)
        purchased.addplayer(name,pos=pos,points=points,cost=cost)
        players.removeplayer(name)
        weights.pop(idx)
        budget -= cost
    return (purchased,budget)

def importSavedData():
    # Load up the player stats list
    f = open('playerstats.pk')
    players = pickle.load(f)
    f.close()
    # Load up exclude lists
    f = open('policeblotter.pk')
    exclude = pickle.load(f)
    f.close()
    f = open('purchased.dat')
    for line in f:
        exclude.append(line.strip('\n'))
    f.close()

    mycash = 200
    teampoints = 0
    # minimunm values
    #nteam = {'QB':2, 'RB':4, 'WR':5, 'TE':3, 'K':2, 'DEF':2}
    # Adding one for a backup
    nteam = {'QB':3, 'RB':5, 'WR':6, 'TE':4, 'K':3, 'DEF':2}
    nplayers = 0
    # Load up the players we've already bought
    # Format should be:
    # Player Name\tPOSITION\tcost
    f = open('myteam.dat')
    for line in f:
        lv = line.split('\t')
        name = lv[0]
        exclude.append(name)
        pos = lv[1]
        mycash -= int(lv[2])        # Used some cash
        nteam[pos] = nteam[pos]-1   # We have one fewer player for that slot
        nplayers += 1
        (yn,idx) = players.getidx(name)
        if yn:
            teampoints += players.points[idx]
    f.close()
    print "Already purchased %d players for $%d. Running with $%d remaining." % (nplayers,200-mycash,mycash)

    # Strip out already purcased players
    for name in exclude:
        players.removeplayer(name)

    return (players,mycash,teampoints,nteam)

if __name__ == "__main__":
    # Load up excluded players and purchased players
    (players,mycash,teampoints,nteam) = importSavedData()
    print "%d Players remaining after exclusion" % (len(players))
    # List all remaining players
    players.listplayers()

    purchased = optimizeRoster(players,mycash,nteam)
    listPurchased(purchased,mycash,teampoints)
