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
MODE_KAGGLE = False
WORKDIR = '.'
# on Kaggle platform :
#WORKDIR = '/kaggle'

def main():
    basedir = WORKDIR
    tempdir = basedir+'/temp/'
    fileextension = 'c_coarse.in.txt'
    listfilein = []
    if MODE_KAGGLE:
        fileextension = '.in'
    #for dirname, _, filenames in os.walk('/kaggle/input'):
    print(basedir+'/input/')
    for dirname, _, filenames in os.walk(basedir+'/input/'):
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


def run_file(filein, fileout, tempdir):

    print(f"Take inputs from : {filein}")

    clients = readfile(filein)
    print(clients)

    # calculate count by ingredient
    like_df = clients['like'].str.split(expand=True).stack().value_counts().reset_index()
    like_df.columns = ['like', 'frequency_like']
    like_df = like_df.set_index('like')
    print(like_df)

    dislike_df = clients['dislike'].str.split(expand=True).stack().value_counts().reset_index()
    dislike_df.columns = ['dislike', 'frequency_dislike']
    dislike_df = dislike_df.set_index('dislike')
    print(dislike_df)

    # left join
    join_df = pd.merge(like_df, dislike_df, how="left", left_index=True, right_index=True).fillna(0)
    print(join_df)

    # filter if dislike >= like
    filter_df = join_df[(join_df['frequency_like'] > join_df['frequency_dislike'])]
    print(filter_df)

    # average
    print(join_df.mean())

    # group by + size/group
    print(join_df.groupby('frequency_like').size())

    # transform
    join_df['sum'] = join_df['frequency_like'] + join_df['frequency_dislike']
    print(join_df)

    # https://www.analyticsvidhya.com/blog/2021/05/pandas-functions-13-most-important/ 
    print(join_df.describe())

    print(filter_df.index.values.tolist())
    outputfile(fileout, filter_df.index.values.tolist())


def readfile(filein):

    f = open(filein, "r")

    # split line 1
    clients_count = int(f.readline())

    # clients (dataframe of Client)
    clients = pd.DataFrame(columns = ['like', 'dislike'])
    i = 0
    for c in range(clients_count):
        array_like = f.readline().split()
        array_dislike = f.readline().split()
        clients.loc[i] = [' '.join(array_like[1:]), ' '.join(array_dislike[1:])]
        i += 1

    f.close()
    return clients


def outputfile(fileout, onepizza_ingredient_list):

    print(f"Write output in: {fileout}")
    fout = open(fileout, "w")
    fout.write(str(len(onepizza_ingredient_list))+' '+" ".join(onepizza_ingredient_list))
    fout.close()


class Client:
    def __init__(self, like, dislike):
        self.like = like
        self.dislike = dislike

    def __repr__(self):
        return str((self.like,self.dislike))


if __name__ == "__main__":
    # execute only if run as a script
    main()
