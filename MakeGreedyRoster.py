# The heavy-lifter program
# This makes our roster using a greedy algorithm for knapsack pakcing
#  Essentially we're maximizing our team value while minimizing cost
#  We also have some constraints like limited QB's, etc.
#  The greedy algorithm doesn't particularlly handle these all too well
#  but it should get us close enough

from PlayerStorage import PlayerStorage
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

# Generate the best roster we can from a playerlist
#  without going over-budget


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
#nteam = {'QB':2, 'RB':5, 'WR':6, 'TE':4, 'K':2, 'DEF':2}
nteam = {'QB':3, 'RB':3, 'WR':3, 'TE':3, 'K':3, 'DEF':3}
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

print "%d Players remaining after exclusion" % (len(players))
# Now make the greedy weights - eg; points/cost
weight = [0]*len(players)
for ii in range(len(players)):
    # Increase this until cash reduces to zero
    fac = 40
    weight[ii] = players.getweight(ii,fac=fac)
    #print repr(players.names[ii]) + "  " + repr(weight[ii])

players.listplayers()
# Now try to maximize our team value
while (mycash > 0) or (not rfilled(nteam)):
    playerscopy = players
    filled = False
    while (not filled):
        maxw = max(weight)
        idx = weight.index(maxw)
        pos = players.pos[idx]
        #print "Searching for %s which has %d remaining slots." % (pos, nteam[pos])
        if nteam[pos] > 0:
            nteam[pos] = nteam[pos]-1
            filled = True
        else:
            weight.pop(idx)
            playerscopy.removeplayer(idx)
    name = players.names[idx]
    cost = players.cost[idx]
    teampoints += players.points[idx]
    mycash -= cost
    print "Purchase %20s to fill %3s for %4d\tTeam worth: %5.2f\tRemaining cash $%d" % (name,pos,cost,teampoints,mycash)
    # When we make a purchase pop the player and weight
    players.removeplayer(name)
    weight.pop(idx)

