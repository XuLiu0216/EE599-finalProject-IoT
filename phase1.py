import math
from datetime import datetime

#The class to represent location
class loc:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#user`s class definition
class UserEntity:
    def __init__(self, id, currLoc, destination, preference, budget, date, startTime, endTime):
        self.id = id
        self.currLoc = currLoc
        #pref = 0 means prefer mincost, pref = 1 means prefer min distance
        self.pref = preference
        #user`s budget for parking
        self.budget = budget
        self.destLoc = destination
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        #the parking choice list for this user
        self.pList = []
        self.opt = -1;

#parking entity`s class
class ParkingEntities:
    def __init__(self, id, loc, charge, maxTime, workday, startTime, endTime, numSpot):
        self.id = id
        self.loc = loc
        self.charge = charge
        self.maxTime = maxTime
        self.workday = workday
        self.startTime = startTime
        self.endTime = endTime
        self.numSpot = numSpot;
        # the user list who would choose this parking structure as an optimal choice
        self.count = 0
        self.uList = []

#The class to represent the interaction between user and parking
class interaction:

    def __init__(self, user, parking):
        self.parking = parking
        self.user = user
    #calculate the distance between user`s current location and the parking structure
    def distance_user_parking(self):
        dis = math.sqrt((self.parking.loc.x - self.user.currLoc.x) ** 2 + (self.parking.loc.y - self.user.currLoc.y) ** 2)
        return dis

    #distance between paking structure and destination
    def walk_distance(self):
        dis = math.sqrt((self.parking.loc.x - self.user.destLoc.x) ** 2 + (self.parking.loc.y - self.user.destLoc.y) ** 2)
        return dis

    #the function to calculate the cost if the user park in this parking entity
    def cost(self):
        #0215 means 2$/hour max 15$/day, assume total cost less than 100$
        hourCharge = int(self.parking.charge[0])*10 + int(self.parking.charge[1])
        dayCharge = int(self.parking.charge[2])*10 + int(self.parking.charge[3])
        if(hourCharge == 0):
            return dayCharge
        elif(dayCharge == 0):
            return hourCharge
        else:
            if dayCharge < hourCharge * (self.user.endTime - self.user.startTime):
                return dayCharge
            else:
                return hourCharge * (self.user.endTime - self.user.startTime)
    #check if there is avaliable parking spots in self parking
    def check(self):
        if self.parking.numSpot <= 0:
            return False
        else:
            weekday = datetime.strptime(self.user.date, "%Y%m%d").weekday()
            if(self.parking.workday[weekday] == '1'):
                if(self.user.startTime >= self.parking.startTime and self.user.endTime <= self.parking.endTime and self.user.endTime - self.user.startTime < self.parking.maxTime):
                    if self.cost() <= self.user.budget and self.walk_distance() <= 1000:
                        return True
            return False

#read the input and save the data
def read_input():
    filename = 'userInput.txt'
    with open(filename, 'r') as f:
        line = f.readline()
        users = {}
        while line:
            id = int(line[0:4])
            userX = int(line[4:8])
            userY = int(line[8:12])
            userLoc = loc(userX, userY)
            destX = int(line[12:16])
            destY = int(line[16:20])
            destLoc = loc(destX, destY)
            pref = int(line[20:21])
            budget = int(line[20:22])
            date = line[22:30]
            start = int(line[30:32])
            end = int(line[32:34])
            user = UserEntity(id, userLoc, destLoc, pref, budget, date, start, end)
            users[id] = user
            line = f.readline()
    f.close()
    filename2 = 'parkingInput.txt'
    with open(filename2, 'r') as f:
        line = f.readline()
        parkings = {}
        while line:
            id = int(line[0:4])
            parkingX = int(line[4:8])
            parkingY = int(line[8:12])
            parkingLoc = loc(parkingX, parkingY)
            charge = line[12:16]
            maxtime = int(line[16:18])
            workday = line[18:25]
            start = int(line[25:27])
            end = int(line[27:29])
            numSpot = int(line[29:33])
            line = f.readline()
            parking = ParkingEntities(id, parkingLoc, charge, maxtime, workday, start, end, numSpot)
            parkings[id] = parking
    f.close()
    return users, parkings

#the process to allocate parking to users
def allocate(U, P):
    numUsers = len(U)#Added to store number of users
    u1 = U[1]
    tempList = []
    M = [[0 for col in range(len(P))] for row in range(len(U))]
    Res = [[0 for col in range(len(P))] for row in range(len(U))]
    pRank = []
    for i in range(len(P)):
        temp = interaction(u1, P[i + 1])
        tempList.append(temp)
    tempList.sort(key=lambda interaction: interaction.walk_distance())
    for t in tempList:
        pRank.append(t.parking.id)

    for m in range(len(U)):
        u = U[m + 1]
        for n in range(len(P)):
            p = P[n + 1]
            i = interaction(u, p)
            if(i.check()):
                M[u.id - 1][p.id - 1] = 1
                p.uList.append(u)
                p.count += 1
                Res[u.id - 1][p.id - 1] = 0
            else:
                Res[u.id - 1][p.id - 1] = 0

    recursiveFunction(U, P, pRank, M , Res)
    #print Res
    #Print out which users go to which parking structures
    for i in range(0,numUsers):
        print "UserID:",i+1 , "Parks in","Parking ID:", Res[i].index(1) +1
    
    return

#The recursive function to solve this problem recursively from the most optimal parking to the least optimal one
#Every time we enter this function we only check the first parking structure in pRank, if there is enough spots,
#the allocate, if not ,then sort all distance between the user who is valid to this parking entity and this
#specific parking
def recursiveFunction(U, P, pRank, M, R):
    #base case to stop
    if len(U) == 0 or len(P) == 0:
        return
    id = pRank[0]
    #no conflict:
    #if there is enough parking spots here
    if P[id].count <= P[id].numSpot:
        for key in U.keys():
            if M[key - 1][id - 1] == 1:
                R[key - 1][id - 1] = 1
                U[key].opt = id
                U.pop(key)
    #if not ,which means there will be several users who wants the same spot => conflict:
    else:
        IA = []
        for key in U.keys():
            if M[key - 1][id - 1] == 1:
                ia = interaction(U[key], P[id])
                IA.append(ia)
        #sort all the users by the distance between user and parking
        IA.sort(key=lambda interaction: interaction.distance_user_parking())
        for j in range(P[id].numSpot):
            userID = IA[j].user.id
            R[userID - 1][id - 1] = 1
            U[userID].opt = id
            U.pop(userID)
            for k in range(id, len(M[0])):
                M[userID - 1][k] = 0
    #delete the parking entity we checked in this round and step into next round
    P.pop(id)
    del(pRank[0])
    return recursiveFunction(U, P, pRank, M, R)


U,P = read_input()
allocate(U,P)

