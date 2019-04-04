import math
from datetime import datetime
import random
import sys

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
    filename = 'inputUser.txt'
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
    filename2 = 'inputParking.txt'
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
    print Res
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

def randSpeed():
    #km/h
    drivingSpeed = random.randint(15,60)
    return drivingSpeed

def get_driving_time(loc1, loc2):
    speed = randSpeed()
    dis = math.sqrt((loc1.x - loc2.x) ** 2 + (loc1.y - loc2.y) ** 2)
    time = math.ceil(dis/speed/1000 * 60)
    return time

def get_walking_time(loc1, loc2):
    # assume walking speed 4500 meters/h
    speed = 4500
    dis = math.sqrt((loc1.x - loc2.x) ** 2 + (loc1.y - loc2.y) ** 2)
    #measured by minitue
    time = math.ceil(dis/speed * 60)
    return time

def bruteforce(U, P):
    for id in U.keys():
        u = U[id]
        meters = 2000
        P = searchParkingWithin(u.destLoc,P, meters)
        min_value = sys.maxint
        min_id = 0
        for id in P.keys():
            p = P[id]
            t1 = get_driving_time(u.currLoc, p.loc)
            t2 = get_walking_time(p.loc, u.destLoc)
            t = t1 + t2
            if t < min_value:
                min_value = t
                min_id = id
        u.opt = min_id
    return

#search for parking spots of the meters within destination
def searchParkingWithin(destLoc, P , meters):
    res = {}
    j = 0
    for id in P.keys():
        p = P[id]
        dis = math.sqrt((destLoc.x - p.loc.x) ** 2 + (destLoc.y - p.loc.y) ** 2)
        if dis <= meters:
            res[id] = p
    return res

def greedy(U, P):
    for id in U.keys():
        u = U[id]
        destination = u.destLoc
        meters = 2000
        P = searchParkingWithin(destination, P, meters)
        des = u.destLoc
        # size = len(P)
        min_value1 = sys.maxint
        min_value2 = sys.maxint
        min_id1 = []
        min_id2 = []
        res = {}
        j = 0
        time1={}
        for id in P.keys():
            p = P[id]
            t1 = get_driving_time(u.currLoc, p.loc)
            time1[id] = t1
            if t1 <= min_value1:
                min_value1 = t1
        for id in time1.keys():
            p = P[id]
            t1 = time1[id]
            if t1 == min_value1:
                min_id1.append(id)
        time2 = {}
        for i in range (len(min_id1)):
            id = min_id1[i]
            t2 = get_walking_time(P[id].loc, u.destLoc)
            time2[id] = t2
            if t2 < min_value2:
                min_value2 = t2
        for id in time2.keys():
            t2 = time2[id]
            if t2 == min_value2:
                min_id2.append(id)
        u.opt = min_id2[0]
    return

#Round Robin Search function finds the first parking spot within walking distance and returns it
def searchParkingWithinRoundRobin(plist, destLoc, P , meters):#special search for round robin
    j = 0
    for id in P.keys():
        p = P[id]
        dis = math.sqrt((destLoc.x - p.loc.x) ** 2 + (destLoc.y - p.loc.y) ** 2)
        if dis <= meters and id not in plist:#check if spot in walking dist, and has not been rejected before
            return id#return first parking spot within walking distance, if its not good enough the user will reject it
    return -1#return -1 if no parking in walking distance

#User decides whether or not to accept the spot
def roundRobinApproval():
    if(random.random() < 0.50):#50% chance of yes
        return 1
    else:
        return 0

'''
Round robin here means that we assign each user a random spot within walking distance
Next the user gets to decide whether or not to accept the spot
If they accept, we give them the spot
If they reject, we put them at the bottom of the queue
'''
def roundRobin(U, P):
    RRqueue = list(U.keys())#make queue of users
    while(len(RRqueue)>0):#while there are still users left in queue
        uid = RRqueue.pop(0)#get first user in queue
        u = U[uid]#store full user object in u
        destination = u.destLoc
        meters = 500#walking distance
        p = searchParkingWithinRoundRobin(u.pList, destination, P, meters)#get random spot within walking distance
        if (p == -1):#this means that there are no spots in walking distance, dont ask if they want it
            u.opt=-1
        elif(roundRobinApproval()):#ask if user wants spots, and if so assign user spot
            u.opt = p
            P[p].numSpot = P[p].numSpot - 1#decrement number of spots at parking location
            if(P[p].numSpot <= 0):#delete spot so other users dont park there
               del P[p]
        else:#add non-accepted spot to users list so we dont offer it again
            u.pList.append(p)#this is a list of rejected spots
            RRqueue.append(uid)#add user to back of queue
            
    return

U,P = read_input()
roundRobin(U,P)
#bruteforce(U,P)
#greedy(U,P)
for id in U.keys():
    u = U[id]
    print u.opt,"opt"

