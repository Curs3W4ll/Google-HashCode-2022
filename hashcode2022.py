#!/usr/bin/env python3

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os

def main():
    basedir = '.'
    #fileextension = 'f_find_great_mentors.in.txt'
    #fileextension = 'a_an_example.in.txt'
    fileextension = '.txt'
    listfilein = []
    print(basedir+'/inputs/')
    for dirname, _, filenames in os.walk(basedir+'/inputs/'):
        for filename in filenames:
            print(os.path.join(dirname, filename))
            pathfilename = os.path.join(dirname, filename)
            if pathfilename.endswith(fileextension):
                listfilein.append((pathfilename, filename))
    for filein, filename in listfilein:
        fileout = basedir+'/output/submission_'+filename
        run_file(filein, fileout)


def run_file(filein, fileout):

    contributors_skills, projects_skills, projects_infos = readfile(filein)
    # print("Contributors skills:")
    # print(contributors_skills)
    # print("\nProjects skills:")
    # print(projects_skills)
    # print("\nProjects infos:")
    # print(projects_infos)
    project_organization = createoutputtable()
    generateoutput(fileout, project_organization)


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
    contrib = []
    for i in range(contributor_count):
        tmp = f.readline()
        contributor_name = tmp.split()[0]
        contributor_skills_count = int(tmp.split()[1])
        for y in range(contributor_skills_count):
            tmp = f.readline()
            skill_name = tmp.split()[0]
            skill_lvl = int(tmp.split()[1])
            #contributors_skills.loc[count] = [contributor_name, skill_name, skill_lvl]
            contrib.append({'name':contributor_name, 'skill_name':skill_name, 'skill_lvl':skill_lvl})
            count += 1
    contributors_skills = pd.DataFrame(contrib)

    count = 0
    subcount = 0
    pji = []
    pjs = []
    for i in range(project_count):
        tmp = f.readline()
        project_name = tmp.split()[0]
        project_duration = int(tmp.split()[1])
        project_award = int(tmp.split()[2])
        project_best_before = int(tmp.split()[3])
        project_skills_nbr = int(tmp.split()[4])
        #projects_infos.loc[subcount] = [project_name, project_duration, project_award, project_best_before, project_skills_nbr]
        pji.append({'name':project_name, 'duration':project_duration, 'award':project_award, 'best_before':project_best_before, 'skills_nbr':project_skills_nbr})
        subcount += 1
        for y in range(project_skills_nbr):
            tmp = f.readline()
            skill_name = tmp.split()[0]
            skill_lvl = int(tmp.split()[1])
            #projects_skills.loc[count] = [project_name, skill_name, skill_lvl, y]
            pjs.append({'name':project_name, 'skill_name':skill_name, 'skill_lvl':skill_lvl, 'skill_pos':y})
            count += 1
    projects_infos = pd.DataFrame(pji)
    projects_skills = pd.DataFrame(pjs)

    return(contributors_skills, projects_skills, projects_infos)


def generateoutput(fileout, project_organization):

    print("About to write organization")
    print(project_organization)
    print(f"\nWrite output in: {fileout}")
    fout = open(fileout, "w")

    fout.write(str(len(project_organization.index)) + '\n')

    project_organization.project_pos.astype(int)
    project_organization = project_organization.sort_values(by=['project_pos'])

    project_organization.reset_index()
    for i, row in project_organization.iterrows():
        fout.write(row['name'] + '\n')
        fout.write(row['contributors'] + '\n')

    fout.close()


def createoutputtable():
    data = [{'contributors': 'Bob Anna', 'name': 'WebServer', 'project_pos':0},
        {'contributors': 'Maria Bob', 'name': 'WebChat', 'project_pos':2},
        {'contributors': 'Anna', 'name': 'Logging', 'project_pos':1},
        ]
    #  project_organization = pd.DataFrame(columns = ['contributors', 'name', 'project_pos'])
    project_organization = pd.DataFrame(data)
    return project_organization


if __name__ == "__main__":
    # execute only if run as a script
    main()
