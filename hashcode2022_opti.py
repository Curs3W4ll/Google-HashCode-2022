#!/usr/bin/env python3

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import math
import os

search_count = 0

def main():
    basedir = '.'
    fileextension = '.txt'
    #fileextension = 'f_find_great_mentors.in.txt'
    #fileextension = 'a_an_example.in.txt'
    #fileextension = 'b_better_start_small.in.txt'
    #fileextension = 'c_collaboration.in.txt'
    listfilein = []
    #print(basedir+'/inputs/')
    for dirname, _, filenames in os.walk(basedir+'/inputs/'):
        for filename in filenames:
            #print(os.path.join(dirname, filename))
            pathfilename = os.path.join(dirname, filename)
            if pathfilename.endswith(fileextension):
                listfilein.append((pathfilename, filename))
    for filein, filename in listfilein:
        fileout = basedir+'/output/submission_'+filename
        run_file(filein, fileout)


def run_file(filein, fileout):

    global search_count

    print(f"Read input in: {filein}")

    search_count = 0

    contributors_skills, projects_skills, projects_infos = readfile(filein)
    organization = createoutputtable()
    organization_list = []

    # reset_index to reorder index by award desc
    projects = projects_infos.sort_values(by=['award'], ascending=False).reset_index()
    #print(projects)

    data_project_skills = projects_skills

    project_skills = pd.DataFrame(data_project_skills)
    # project_skill = {'name': 'Logging', 'skill_name': 'C++', 'skill_lvl':5, 'skill_pos':0}

    for inc in range(projects.index.size):
        proj_name = projects.loc[inc]['name']
        #print("====> " + proj_name)

        # optimisation : remove is_faisable and manage it directly in assign_worker_to_role
        #if is_faisable(contributors_skills, project_skills, proj_name):
        project_skills_list = project_skills[(project_skills['name'] == proj_name)]
        organization_list = assign_worker_to_role(contributors_skills, project_skills_list, proj_name, organization_list)

    print('search_count:' + str(search_count))
    #generateoutput(fileout, organization)
    generateoutput_fromlist(fileout, organization_list)


def add_to_organization(organization, contributor, project_name):
    row = organization[(organization['name'] == project_name)]
    contributor_name = contributor['name'].iloc[0]
    last_pos = organization['project_pos'].max()
    if math.isnan(last_pos):
        last_pos = 0
    if row.empty:
        new_row = pd.DataFrame([{'name': project_name, 'contributors': contributor_name, 'project_pos': last_pos + 1}])
        organization = pd.concat([organization, new_row], ignore_index = True)
    else:
        organization.loc[row.index, 'contributors'] = organization.loc[row.index, 'contributors'] + ' ' + contributor_name
    return organization


def assign_worker_to_role(contributors, project_skills, project_name, organization_list):

    global search_count
    is_all_contributors = True
    list_contributor = []

    #print(project_skills['skill_name'].values)
    df_skill = contributors[contributors['skill_name'].isin(project_skills['skill_name'].values)].set_index("name")
    #print(df_skill)
    #print(contributors)
    for n in project_skills.index:
        project_skill = project_skills.loc[n]
        skill_name = project_skill['skill_name']
        skill_lvl = project_skill['skill_lvl']
        search_count += 1

        good_contributor = df_skill[(df_skill['skill_name'] == skill_name) & (df_skill['skill_lvl'] >= skill_lvl)].head(1)
        #print(good_contributor)

        if good_contributor.index.size >= 1:
            contrib_name = good_contributor.index.values[0]
            # remove the contrib name
            df_skill = df_skill.drop(contrib_name)
            # add to list_contributor
            list_contributor.append(contrib_name)
        else:
            is_all_contributors = False
            break

    if is_all_contributors:
        # concat tmp_organization to global organization
        organization_list.append((project_name, " ".join(list_contributor)))

    return organization_list


def get_contributors_with_skill(contributors, skill, lvl):

    return contributors[(contributors["skill_name"]==skill) &
                                         (contributors["skill_lvl"]>=lvl) &
                                         (contributors["dispo"])]

def assign(assigned, contributors):
    for i, row in contributors.iterrows():
        if not row["name"] in assigned:
            assigned.append(row["name"])
            return assigned
    return []

def is_faisable(contributors, projects_skills, project):

    project_skills = projects_skills[(projects_skills["name"]==project)]
    assigned = []
    #print(project_skills)

    for i, row in project_skills.iterrows():
        assigned = assign(assigned, get_contributors_with_skill(contributors, row["skill_name"], row["skill_lvl"]))
        if assigned == []:
            return False;
    return True


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
    #  print(project_organization)
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

def generateoutput_fromlist(fileout, organization_list):

    print(f"\nWrite output in: {fileout}")
    fout = open(fileout, "w")

    fout.write(str(len(organization_list)) + '\n')

    for p in organization_list:
        fout.write(p[0] + '\n')
        fout.write(p[1] + '\n')

    fout.close()


def createoutputtable():
    project_organization = pd.DataFrame(columns = ['name', 'contributors', 'project_pos'])
    return project_organization


if __name__ == "__main__":
    # execute only if run as a script
    main()
