import math
from datetime import datetime
class loc:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class UserEntity:
    def __init__(self, id, currLoc, destination, preference, budget, carModel, date, startTime, endTime):
        self.id = id
        self.currLoc = currLoc
        #pref = 0 means prefer mincost, pref = 1 means prefer min distance
        self.pref = preference
        #user`s budget for parking
        self.budget = budget
        self.destLoc = destination
        self.carModel = carModel
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        #the parking choice list for this user
        self.plist = []

class ParkingEntities:
    def __init__(self, id, loc, charge, maxTime, workday, startTime, endTime, numCompact, numRegular):
        self.id = id
        self.loc = loc
        self.charge = charge
        self.maxTime = maxTime
        self.workday = workday
        self.startTime = startTime
        self.endTime = endTime
        self.numCompact = numCompact
        self.numRegular = numRegular
        #the user list who would choose this parking structure as an optimal choice
        self.uList = []

class interaction:

    def __init__(self, user, parking):
        self.parking = parking
        self.user = user

    def distance_user_parking(self):
        dis = math.sqrt((self.parking.loc.x - self.user.loc.x) ** 2 + (self.parking.loc.y - self.user.loc.y) ** 2)
        return dis

    #distance between paking structure and destination
    def walk_distance(self):
        dis = math.sqrt((self.parking.loc.x - self.user.destLoc.x) ** 2 + (self.parking.loc.y - self.user.destLoc.y) ** 2)
        return dis

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
    def check_avaliable(self):
        #model only includes'S' and 'R', S means small, R means regular.
        #compact paking spaces only for small cars, and regular paking spots serve for small and regular cars both
        model = self.user.carModel
        if(model =='S' and (self.parking.numCompact + self.parking.numRegular) <= 0):
            return False
        elif(model == 'R' and self.parking.numRegular <= 0):
            return False
        else:
            weekday = datetime.strptime(self.user.date, "%Y%m%d").weekday()
            if(self.parking.workday[weekday] == '1'):
                if(self.user.startTime >= self.parking.startTime and self.user.endTime <= self.parking.endTime and self.user.endTime - self.user.startTime < self.parking.maxTime):
                    return True
            return False

    #final check : if the avaliable parking spot suit for user`s preference
    def check(self):
        if(self.check_avaliable()):
            if(self.user.pref == 0):
                print self.cost()
                if(self.cost() <= self.user.budget):
                    return True
            else:
                #assume we only choose the parking less than 1000 meters
                if(self.walk_distance() <= 10000):
                    return True
        return False



    def __lt__(self, other):
        if self.walk_distance() < other.walk_distance():
            return True;
        else:
            return False;

def read_input():
    filename = 'userInput.txt'
    with open(filename, 'r') as f:
        line = f.readline()
        users = []
        while line:
            id = line[0:4]
            userX = int(line[4:8])
            userY = int(line[8:12])
            userLoc = loc(userX, userY)
            destX = int(line[12:16])
            destY = int(line[16:20])
            destLoc = loc(destX, destY)
            pref = int(line[20:21])
            budget = int(line[21:23])
            model = line[23:24]
            date = line[24:32]
            start = int(line[32:34])
            end = int(line[34:36])
            user = UserEntity(id, userLoc, destLoc, pref, budget, model, date, start, end)
            users.append(user)
            line = f.readline()
    f.close()
    filename2 = 'parkingInput.txt'
    with open(filename2, 'r') as f:
        line = f.readline()
        parkings = []
        while line:
            id = line[0:4]
            parkingX = int(line[4:8])
            parkingY = int(line[8:12])
            parkingLoc = loc(parkingX, parkingY)
            charge = line[12:16]
            maxtime = int(line[16:18])
            workday = line[18:25]
            start = int(line[25:27])
            end = int(line[27:29])
            numCompact = int(line[29:33])
            numRegular = int(line[33:37])
            line = f.readline()
            parking = ParkingEntities(id, parkingLoc, charge, maxtime, workday, start, end, numCompact, numRegular)
            parkings.append(parking)
    f.close()
    return users, parkings


U,P = read_input()
#UI is the list of list of interactions for each user
UI = []
for u in U:
    #I is the list of interactions for this user u
    I = []
    for p in P:
        i = interaction(u, p)
        if(i.check()):
            I.append(i)
    if(I[0].user.pref == 0):
        I.sort(key = lambda interaction: interaction.cost())
    else:
        I.sort(key = lambda interaction: interaction.walk_distance())
    UI.append(I)
