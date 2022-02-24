#!/bin/env python3

import pandas as pd


def readfile(filein):

    f = open(filein, "r")

    tmp = f.readline()
    contributor_count = int(tmp.split()[0])
    project_count = int(tmp.split()[1])
    print("Their is", contributor_count, "contributors and", project_count, "projects\n")

    contributors_skills = pd.DataFrame(columns = ['name', 'skill_name', 'skill_lvl'])
    projects_skills = pd.DataFrame(columns = ['name', 'skill_name', 'skill_lvl', 'skill_pos'])
    projects_infos = pd.DataFrame(columns = ['name', 'duration', 'award', 'best_before', 'skills_nbr'])

    count = 0
    for i in range(contributor_count):
        tmp = f.readline()
        contributor_name = tmp.split()[0]
        contributor_skills_count = int(tmp.split()[1])
        for y in range(contributor_skills_count):
            tmp = f.readline()
            skill_name = tmp.split()[0]
            skill_lvl = int(tmp.split()[1])
            contributors_skills.loc[count] = [contributor_name, skill_name, skill_lvl]
            count += 1

    count = 0
    subcount = 0
    for i in range(project_count):
        tmp = f.readline()
        project_name = tmp.split()[0]
        project_duration = int(tmp.split()[1])
        project_award = int(tmp.split()[2])
        project_best_before = int(tmp.split()[3])
        project_skills_nbr = int(tmp.split()[4])
        projects_infos.loc[subcount] = [project_name, project_duration, project_award, project_best_before, project_skills_nbr]
        subcount += 1
        for y in range(project_skills_nbr):
            tmp = f.readline()
            skill_name = tmp.split()[0]
            skill_lvl = int(tmp.split()[1])
            projects_skills.loc[count] = [project_name, skill_name, skill_lvl, y]
            count += 1

    print("Contributors skills:")
    print(contributors_skills)

    print("\nProjects skills:")
    print(projects_skills)

    print("\nProjects infos:")
    print(projects_infos)

if __name__ == "__main__":
    readfile("inputs/a_an_example.in.txt")
