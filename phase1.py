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
        self.pref = preference
        self.budget = budget
        self.destLoc = destination
        self.carModel = carModel
        self.date = date
        self.startTime = startTime
        self.endTime = endTime

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

    def check_valid(self):
        model = self.user.carModel
        if(model =='S' and (self.parking.numCompact + self.parking.numRegular) <= 0):
            print "1"
            return False
        elif(model == 'R' and self.parking.numRegular <= 0):
            print"2"
            return False
        else:
            weekday = datetime.strptime(self.user.date, "%Y%m%d").weekday()
            if(self.parking.workday[weekday] == '1'):
                print self.user.startTime
                if(self.user.startTime >= self.parking.startTime and self.user.endTime <= self.parking.endTime and self.user.endTime - self.user.startTime < self.parking.maxTime):
                    return True
            print"3"
            return False

    def cost(self):
        #0215 means 2$/hour max 15$/day, assume total cost less than 100$
        hourCharge = self.parking.charge[0]*10 + self.parking.charge[1]
        dayCharge = self.parking.charge[2]*10 + self.parking.charge[3]
        if(hourCharge == 0):
            return dayCharge
        elif(dayCharge == 0):
            return hourCharge
        else:
            if dayCharge < hourCharge * (self.user.endTime - self.user.startTime):
                return dayCharge
            else:
                return hourCharge * (self.user.endTime - self.user.startTime)


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
            print numRegular
            line = f.readline()
            parking = ParkingEntities(id, parkingLoc, charge, maxtime, workday, start, end, numCompact, numRegular)
            parkings.append(parking)
    f.close()
    return users, parkings

U,P = read_input()
I = []
for p in P:
    i = interaction(U[0], p)
    I.append(i)

def inter_cmp(i1, i2):
    return int(i1.walk_distance() - i2.walk_distance())

I.sort(cmp = inter_cmp)
print I[0].walk_distance(),I[1].walk_distance(),I[2].walk_distance(),I[3].walk_distance(),
