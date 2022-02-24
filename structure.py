#!/usr/bin/env python3

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

def main():
    df_contrib_skills = create_df_contrib_sample()
    print(df_contrib_skills)

def create_df_contrib_sample():
    data = [{'name': 'Anna', 'skill_name': 'C++', 'skill_lvl':2},
        {'name': 'Bob', 'skill_name': 'HTML', 'skill_lvl':5},
        {'name': 'Bob', 'skill_name': 'CSS', 'skill_lvl':5},
        {'name': 'Maria', 'skill_name': 'Python', 'skill_lvl':3},
        ]
    df = pd.DataFrame(data)
    return(df)

if __name__ == "__main__":
    # execute only if run as a script
    main()