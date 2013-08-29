# This defines a class that holds the player names, positions, points
#  and expected cost for a budget of $200
# Has useful methods for adding, removing and updaing players
#  TODO: I think the update method is broken

class PlayerStorage():
    def __init__(self):
        self.names = []
        self.pos = []
        self.points = []
        self.cost = []
        return

    def __len__(self):
        return len(self.names)

    # We require at least a player name to add a player
    def addplayer(self,name,pos='',points=0,cost=0):
        self.names.append(name)
        self.pos.append(pos)
        self.points.append(points)
        self.cost.append(cost)
        return

    # Get the index of a particular player
    def getidx(self,get):
        foundyn = True
        mytype = type(get)
        idx = 0
        if (mytype is str) or (mytype is unicode):
            try:
                idx = self.names.index(get)
            except ValueError:
                foundyn = False
        else:
            idx = get
        return (foundyn,idx)

    # Get stats for a specific player
    def getplayer(self,get):
        (idxyn,idx) = self.getidx(get)
        if idxyn:
            rv = (self.names[idx],self.pos[idx],self.points[idx],self.cost[idx])
        else:
            rv = ('','',0.0,0)
        return rv

    # Removal can be by name or by position
    def removeplayer(self,get):
        (idxyn,idx) = self.getidx(get)
        if idxyn:
            self.names.pop(idx)
            self.pos.pop(idx)
            self.points.pop(idx)
            self.cost.pop(idx)
        return

    # Update by removing and re-adding
    def updateplayer(self,name,pos='',points=0.0,cost=0):
        self.removeplayer(name)
        self.addplayer(name,pos=pos,points=points,cost=cost)
        return

    # Copy the elements of the class into a new one
    # Needed a value copy for repetitive iteration of roster finding
    def copy(self):
        copy = PlayerStorage()
        for idx in range(len(self)):
            (name,pos,points,cost) = self.getplayer(idx)
            copy.addplayer(name,pos=pos,points=points,cost=cost)
        return copy

    # Get the weight (points/cost) for all players
    def getweight(self,fac=1):
        weight = [0]*len(self)
        for idx in range(len(self)):
            cost = self.cost[idx]/fac + 1
            weight[idx] = self.points[idx]/cost
        return weight

    # Useful to dump the contents if we're debugging
    def listplayers(self):
        for ii in range(len(self.names)):
            print '%25s%4s%15.2f%5d' % \
                (self.names[ii], self.pos[ii], self.points[ii], \
                 self.cost[ii])
        return
