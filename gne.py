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


def main():
    contributors = create_df_contrib_sample()
    contributors['dispo'] = True
    contributors['skill_assigned_to'] = ""
    project_skill = {'name': 'Logging', 'skill_name': 'C++', 'skill_lvl':5, 'skill_pos':0}
    assign_worker_to_role(contributors, project_skill)

def create_df_contrib_sample():
    data = [{'name': 'Anna', 'skill_name': 'C++', 'skill_lvl':2},
        {'name': 'Bob', 'skill_name': 'HTML', 'skill_lvl':5},
        {'name': 'Bob', 'skill_name': 'CSS', 'skill_lvl':5},
        {'name': 'Maria', 'skill_name': 'Python', 'skill_lvl':3},
        {'name': 'Jean', 'skill_name': 'C++', 'skill_lvl':8},
        ]
    df = pd.DataFrame(data)
    return(df)

def assign_worker_to_role(contributors, project_skill):
    like_df = contributors['name'].str.split(expand=True).stack().value_counts().reset_index()
    like_df.columns = ['name', 'id']
    nb_worker = like_df['name'].drop_duplicates().size

    good_contributor = contributors[(contributors['skill_name'] == project_skill['skill_name']) &
                                    (contributors['skill_lvl'] >= project_skill['skill_lvl'])   &
                                    (contributors['dispo'] == True)].head(1)

    if good_contributor.index.size >= 1:
        print(good_contributor)
        good_contributor.loc[good_contributor.index, ['dispo']] = False
        good_contributor.loc[good_contributor.index, ['skill_assigned_to']] = project_skill['skill_name']
    print(good_contributor)


if __name__ == "__main__":
    main()
