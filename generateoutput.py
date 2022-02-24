#!/bin/env python3

import pandas as pd


def createoutputtable():
    data = [{'contributors': 'Bob Anna', 'name': 'WebServer', 'project_pos':0},
        {'contributors': 'Maria Bob', 'name': 'WebChat', 'project_pos':2},
        {'contributors': 'Anna', 'name': 'Logging', 'project_pos':1},
        ]
    #  project_organization = pd.DataFrame(columns = ['contributors', 'name', 'project_pos'])
    project_organization = pd.DataFrame(data)
    return project_organization


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

if __name__ == "__main__":
    project_organization = createoutputtable()
    generateoutput("toto.tmp.txt", project_organization)
