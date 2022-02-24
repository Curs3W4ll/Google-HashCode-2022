#!/usr/bin/env python3
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

# MODE_KAGGLE => specific basedir / filein = *.in / fileout = submission.csv
# ELSE => filein = *.txt / fileout = submission_samefilein
MODE_KAGGLE = True
WORKDIR = '/Users/laurent.hervaud/Documents/kaggle'
# on Kaggle platform :
#WORKDIR = '/kaggle'
# max duration of green lights
DURATION_MAX = 1

def main():
    basedir = WORKDIR
    tempdir = basedir+'/temp/'
    fileextension = '.txt'
    listfilein = []
    if MODE_KAGGLE:
        fileextension = '.in'
    #for dirname, _, filenames in os.walk('/kaggle/input'):
    for dirname, _, filenames in os.walk(basedir+'/input'):
        for filename in filenames:
            #print(os.path.join(dirname, filename))
            pathfilename = os.path.join(dirname, filename)
            if pathfilename.endswith(fileextension):
                listfilein.append((pathfilename, filename))
    for filein, filename in listfilein:
        if MODE_KAGGLE:
            fileout = basedir+'/working/submission.csv'
        else:
            fileout = basedir+'/working/submission_'+filename
        run_file(filein, fileout, tempdir)

    # You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
    # You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session
    # Submission file must be named submission.csv

# take load element for sort
def takeLoad(street_schedule):
    return street_schedule.traffic.load

# take firstinpath_count element for sort
def takeFirstStreetPathCount(street_schedule):
    return street_schedule.traffic.firstinpath_count

def run_file(filein, fileout, tempdir):

    print(f"Take inputs from : {filein}")

    f = open(filein, "r")

    # split line 1
    line1 = f.readline()
    l1 = line1.split()
    total_duration = int(l1[0])
    inter_count = int(l1[1])
    street_count = int(l1[2])
    car_count = int(l1[3])
    bonus = int(l1[4])

    # max duration of green lights
    max_duration = DURATION_MAX
    if max_duration > total_duration/2:
        max_duration = total_duration/2

    # streets (dict of Street)
    streets = dict()
    for s in range(street_count):
        array_line = f.readline().split()
        streets[array_line[2]] = Street(array_line[2], array_line[0], array_line[1], array_line[3])

    print(f"streets: {len(streets):,}")
    #print(streets)

    # cars (list of Car)
    cars = []
    for c in range(car_count):
        array_line = f.readline().split()
        cars.append(Car(int(array_line[0]), array_line[1:int(array_line[0])+1]))

    print(f"cars: {len(cars):,}")
    #print(cars)

    f.close()

    # calculate car_count by street (dict of Traffic)
    traffic = dict()
    for c in cars:
        # fix : remove last street for each car (no need to be count as trafic because no light needed)
        first_street = 1
        for s in c.streets_path[:-1]:
            if s in traffic:
                traffic[s].load += 1
                traffic[s].firstinpath_count += first_street
            else:
                traffic[s] = Traffic(1, first_street)
            first_street = 0

    print(f"traffic: {len(traffic):,}")

    # intersections (dict of only end of street) => dict of intersection eg list(streetname)
    intersections = dict()
    for skey, svalue in streets.items():
        if svalue.i_end in intersections:
            intersections[svalue.i_end].streets.append(skey)
        else:
            list_street = []
            list_street.append(skey)
            intersections[svalue.i_end] = Intersection(skey, list_street)

    print(f"intersections: {len(intersections):,}")

    # calculate for each intersection/street traffic
    schedules = dict()
    for skey, svalue in intersections.items():
        street_load = []
        for s in svalue.streets:
            if s in traffic:
                street_load.append(StreetSchedule(streets[s], traffic[s], 0))
        if len(street_load) > 0:
            street_load.sort(key=takeLoad, reverse=True)
        
        street_schedule = []
        # start at max_duration
        duration = max_duration
        load_pred = 0
        first_duration = True
        for sc in street_load:
            if first_duration == False:
                # duration proportional as load(pred) / load(actual)
                duration = duration / (load_pred/sc.traffic.load)
                if duration < 1:
                    duration = 1
            else:
                first_duration = False
            street_schedule.append(StreetSchedule(sc.street, sc.traffic, int(duration)))
            load_pred = sc.traffic.load

        # sort street list by first street count in car path
        street_schedule.sort(key=takeFirstStreetPathCount, reverse=True)

        if len(street_schedule) > 0:
            schedules[skey] = street_schedule

    print(f"schedules: {len(schedules):,}")
    #print(schedules)

    # restit
    print(f"Write output in: {fileout}")
    fout = open(fileout, "w")
    fout.write(str(len(schedules))+'\n')
    for skey, svalue in schedules.items():
        fout.write(skey+'\n')
        fout.write(str(len(svalue))+'\n')
        for street_schedule in svalue:
            fout.write(street_schedule.street.name+' '+str(street_schedule.duration)+'\n')

    fout.close()
    print(f"Cars count: {car_count:,}")
    print(f"Bonus points by car: {bonus:,}")

    # simulation
    score = simulation(total_duration, bonus, schedules, cars, streets, tempdir)

    print(f"Score: {score:,}\n")


def simulation(total_duration, bonus, schedules, cars, streets, tempdir):

    car_finished = 0 # counts how many cars have finished their path    

    # prepare cars position (-1 for end of street), store T in second
    # car_pos = (list[street], position in street (1 to len), T)
    # remove street from list where finished => is street list is empty, 
    # car finished is path and T is blocked to compute score at the end
    for c in cars:
        c.streets_current = c.streets_path
        c.position = -1 #(-1 for end of first street)
        c.time_finish = -1
    #print(cars)

    # prepare schedule state : for each intersection, store state (True=car passed, False=no car passed),
    # list of street and second for green light
    # schedule_state = (state, list[(street, second left for green light)])
    # when second left is 0, remove street from list
    # when list is empty, reload street list from schedules
    schedules_state = dict()
    for intersection, sched in schedules.items():
        street_list = []
        schedules_state[intersection] = IntersectionScheduleState(False, sched, sched[0].duration)

    #print(schedules_state)
 
    # compute for each second : car position, schedules light position
    for t in range(0, total_duration):
        for c in cars:
            if c.time_finish == -1:
                if c.position == -1:
                    # check intersection state
                    if streets[c.streets_current[0]].i_end in schedules_state:
                        sched_state = schedules_state[streets[c.streets_current[0]].i_end]
                        if sched_state.car_passed == False and sched_state.streets_list[0].street.name == c.streets_current[0]:
                            # current car can pass
                            # remove the street from list
                            c.streets_current = c.streets_current[1:]
                            if not c.streets_current:
                                # path finished, store time
                                c.time_finish = t
                                c.position = -1
                                car_finished += 1
                            else:
                                # store 1 as position
                                c.position = 1
                            # change state of intersection
                            sched_state.car_passed = True                    
                        else:
                            # car is waiting
                            pass
                else:
                    # car moving forward
                    c.position += 1

                # check if street is finished
                if c.position >= streets[c.streets_current[0]].length:
                    c.position = -1
                    # check if it's the last street
                    if len(c.streets_current) == 1:
                        # path finished, store time
                        c.streets_current = []
                        c.time_finish = t
                        car_finished += 1

        #print(f"T: {t:,}")
        #print(cars)
        #print(schedules_state)

        # pass state to True and remove 1 second for each intersection in schedules_state
        for intersection, sched_state in schedules_state.items():
            sched_state.car_passed = False
            sched_state.time_left -= 1
            if sched_state.time_left == 0:
                # remove street from schedule
                sched_state.streets_list = sched_state.streets_list[1:]
                if not sched_state.streets_list:
                    # schedule is finished
                    sched_state.streets_list = schedules[intersection]
                sched_state.time_left = sched_state.streets_list[0].duration
            #print(sched_state)

        # print cars finished
        if t%100 == 0:
            print(f"T={t:,} | cars finished: {car_finished:,}")

    # sum of score
    total_score = 0
    for c in cars:
        car_score = 0
        if c.time_finish > -1:
            car_score = bonus + (total_duration - c.time_finish)
        total_score += car_score

    # write temp file
    print(f"Write temp in: {tempdir}")
    fcar = open(tempdir+'cars_state.txt', "w")
    fcar.write('streets\tposition\ttime_finish\n')
    fcar_run = open(tempdir+'cars_run.txt', "w")
    fcar_run.write('street\tposition\n')
    for c in cars:
        fcar.write(str(c.streets_current))
        fcar.write('\t'+str(c.position)+'\t'+str(c.time_finish)+'\n')
        if c.time_finish == -1:
            fcar_run.write(c.streets_current[0]+'\t'+str(c.position)+'\n')

    fcar.close()
    fcar_run.close()

    return(total_score)


class Street:
    def __init__(self, name, i_start, i_end, length):
        self.name = name
        self.i_start = i_start
        self.i_end = i_end
        self.length = int(length)

    def __repr__(self):
        return str((self.name,self.i_start,self.i_end,self.length))


class Car:
    def __init__(self, street_count, streets_array):
        self.street_count = street_count
        self.streets_path = streets_array

    streets_current = [] # for simulation
    position = -1 #(-1 for end of street)
    time_finish = -1 # for score calculation at the end of simulation

    def __repr__(self):
        return str((self.street_count,self.streets_path,self.streets_current,self.position,self.time_finish))


class Traffic:
    def __init__(self, load, firstinpath_count):
        self.load = load
        self.firstinpath_count = firstinpath_count

    def __repr__(self):
        return str((self.load,self.firstinpath_count))


class StreetSchedule:
    def __init__(self, street, traffic, duration):
        self.street = street
        self.traffic = traffic
        self.duration = duration

    def __repr__(self):
        return str((self.street,self.traffic,self.duration))


class Intersection:
    def __init__(self, index, streets_list):
        self.index = index
        self.streets = streets_list

    def __repr__(self):
        return str((self.index,self.streets_list))


class IntersectionScheduleState:
    def __init__(self, car_passed, streets_list, time_left):
        self.car_passed = car_passed
        self.streets_list = streets_list
        self.time_left = time_left    

    def __repr__(self):
        return str((self.car_passed,self.streets_list,self.time_left))


if __name__ == "__main__":
    # execute only if run as a script
    main()
