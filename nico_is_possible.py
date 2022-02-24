#!/usr/bin/env python3

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

def get_contributors_with_skill(contributors, skill, lvl):

    return contributors[(contributors["skill_name"]==skill) &
                                         (contributors["skill_lvl"]>=lvl) &
                                         (contributors["dispo"]==True)]

def assign(assigned, contributors):
    for i, row in contributors.iterrows():
        print(row)
        if not row["name"] in assigned:
            assigned.append(row["name"])
            return assigned
    return []

def is_possible(contributors, projects_skills, project):

    project_skills = projects_skills[(projects_skills["name"]==project)]
    assigned = []
    #print(project_skills)

    for i, row in project_skills.iterrows():
        assigned = assign(assigned, get_contributors_with_skill(contributors, row["skill_name"], row["skill_lvl"]))
        if assigned == []:
            return False;
    return True

def available_skills(contributors, project):

    contributors_list = contributors[(contributors["skill_name"]==project["skill_name"]) &
                                     (contributors["skill_lvl"]>=project["skill_lvl"]) &
                                     (contributors["dispo"]==True)]

    nb_contributors = len(contributors_list.index)
    if (nb_contributors == 0):
        return False
    return True


def main():
    df_contribs_skills = create_df_contrib_sample()
    #print(df_contribs_skills)
    df_projects_skills = create_df_project_skill_sample()
    #print(df_projects_skills)
    df_projects_infos = create_df_project_info_sample()
    #print(df_projects_infos)

    df_contribs_skills["dispo"] = True

    print(is_possible(df_contribs_skills, df_projects_skills, "WebServer"))
    print(df_contribs_skills)
    #print(available_skills(df_contribs_skills, df_projects_skills.iloc[2]))



def create_df_contrib_sample():
    data = [{'name': 'Bob', 'skill_name': 'HTML', 'skill_lvl':5},
        {'name': 'Bob', 'skill_name': 'C++', 'skill_lvl':5},
        {'name': 'Anna', 'skill_name': 'C++', 'skill_lvl':2},
        {'name': 'Maria', 'skill_name': 'Python', 'skill_lvl':3},
        ]
    df = pd.DataFrame(data)
    return(df)


def create_df_project_skill_sample():
    data = [{'name': 'Logging', 'skill_name': 'C++', 'skill_lvl':3, 'skill_pos':0},
        {'name': 'WebServer', 'skill_name': 'HTML', 'skill_lvl':3, 'skill_pos':0},
        {'name': 'WebServer', 'skill_name': 'C++', 'skill_lvl':2, 'skill_pos':1},
        {'name': 'WebChat', 'skill_name': 'Python', 'skill_lvl':3, 'skill_pos':0},
        {'name': 'WebChat', 'skill_name': 'HTML', 'skill_lvl':3, 'skill_pos':1}
        ]
    df = pd.DataFrame(data)
    return(df)


def create_df_project_info_sample():
    data = [{'name': 'Logging', 'duration': 5, 'award':10, 'best_time':5, 'skills_nbr':1},
        {'name': 'WebServer', 'duration': 7, 'award':10, 'best_time':7, 'skills_nbr':2},
        {'name': 'WebChat', 'duration': 10, 'award':20, 'best_time':20, 'skills_nbr':2}
        ]
    df = pd.DataFrame(data)
    return(df)


if __name__ == "__main__":
    # execute only if run as a script
    main()
