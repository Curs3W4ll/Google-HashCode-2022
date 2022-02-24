#!/usr/bin/env python3

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

def main():
    df_contribs_skills = create_df_contrib_sample()
    print(df_contribs_skills)
    df_projects_skills = create_df_project_skill_sample()
    print(df_projects_skills)
    df_projects_infos= create_df_project_info_sample()
    print(df_projects_infos)


def create_df_contrib_sample():
    data = [{'name': 'Anna', 'skill_name': 'C++', 'skill_lvl':2},
        {'name': 'Bob', 'skill_name': 'HTML', 'skill_lvl':5},
        {'name': 'Bob', 'skill_name': 'CSS', 'skill_lvl':5},
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