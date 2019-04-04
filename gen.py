import random
from datetime import datetime

userNum = 1000
filename = 'inputUser.txt'
with open (filename, 'w') as f:
    for i in range(0, userNum):
        if i > 999:
            f.write(str(i))
        elif i > 99:
            f.write('0' + str(i))
        elif i > 9:
            f.write('00' + str(i))
        else:
            f.write('000' + str(i))
        curr_x = random.randint(0, 9999)
        if curr_x > 999:
            f.write(str(curr_x))
        elif curr_x > 99:
            f.write('0' + str(curr_x))
        elif curr_x > 9:
            f.write('00' + str(curr_x))
        else:
            f.write('000' + str(curr_x))
        curr_y = random.randint(0, 9999)
        if curr_y > 999:
            f.write(str(curr_y))
        elif curr_y > 99:
            f.write('0' + str(curr_y))
        elif curr_y > 9:
            f.write('00' + str(curr_y))
        else:
            f.write('000' + str(curr_y))
        dest_x = random.randint(0, 9999)
        if dest_x > 999:
            f.write(str(dest_x))
        elif dest_x > 99:
            f.write('0' + str(dest_x))
        elif dest_x > 9:
            f.write('00' + str(dest_x))
        else:
            f.write('000' + str(dest_x))
        dest_y = random.randint(0, 9999)
        if dest_y > 999:
            f.write(str(dest_y))
        elif dest_y > 99:
            f.write('0' + str(dest_y))
        elif dest_y > 9:
            f.write('00' + str(dest_y))
        else:
            f.write('000' + str(dest_y))

        budget = random.randint(10, 20)
        f.write(str(budget))
        year = datetime.now().year
        f.write(str(year))
        month = datetime.now().month
        if month > 9:
            f.write(str(month))
        else:
            f.write('0' + str(month))
        day = datetime.now().day
        if day > 9:
            f.write(str(day))
        else:
            f.write('0' + str(day))
        hour = datetime.now().hour
        if hour > 9:
            f.write(str(hour))
        else:
            f.write('0' + str(hour))
        duration = random.randint(1,4)
        endHour = hour + duration
        if endHour > 9:
            f.write(str(endHour))
        else:
            f.write('0' + str(endHour))
        f.write('\n')
    f.close()

    parkingNum = 1000
    filename = 'inputParking.txt'
    with open(filename, 'w') as f:
        for i in range(0, parkingNum):
            if i > 999:
                f.write(str(i))
            elif i > 99:
                f.write('0' + str(i))
            elif i > 9:
                f.write('00' + str(i))
            else:
                f.write('000' + str(i))
            parking_x = random.randint(0, 9999)
            if parking_x > 999:
                f.write(str(parking_x))
            elif parking_x > 99:
                f.write('0' + str(parking_x))
            elif parking_x > 9:
                f.write('00' + str(parking_x))
            else:
                f.write('000' + str(parking_x))
            parking_y = random.randint(0, 9999)
            if parking_y > 999:
                f.write(str(parking_y))
            elif parking_y > 99:
                f.write('0' + str(parking_y))
            elif parking_y > 9:
                f.write('00' + str(parking_y))
            else:
                f.write('000' + str(parking_y))
            hourCharge = random.randint(0,5)
            f.write('0'+ str(hourCharge))
            dayCharge = random.randint(15, 30)
            f.write(str(dayCharge))
            durationList = [1,2,3,4,24]
            duration = durationList[random.randint(0, 4)]
            if duration > 9:
                f.write(str(duration))
            else:
                f.write('0' + str(duration))

            workModes = ["1111100", "1111110", "1111111"]
            f.write(workModes[random.randint(0,2)])
            startEnd = ["0817", "0918", "0922"]
            if duration == 24:
                f.write("0024")
            else:
                f.write(startEnd[random.randint(0, 2)])
            numSpots = random.randint(0, 100)
            if numSpots > 999:
                f.write(str(numSpots))
            elif numSpots > 99:
                f.write('0' + str(numSpots))
            elif numSpots > 9:
                f.write('00' + str(numSpots))
            else:
                f.write('000' + str(numSpots))
            f.write('\n')
        f.close()


