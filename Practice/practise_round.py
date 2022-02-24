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
    fileextension = '.txt'
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
    #print(clients)

    # calculate count by ingredient
    like_ingredient = dict()
    dislike_ingredient = dict()
    for c in clients:
        for i in c.like:
            if i in like_ingredient:
                like_ingredient[i] += 1
            else:
                like_ingredient[i] = 1
        for i in c.dislike:
            if i in dislike_ingredient:
                dislike_ingredient[i] += 1
            else:
                dislike_ingredient[i] = 1

    #print(like_ingredient)
    #print(dislike_ingredient)

    # remove from like if dislike >=
    for i in like_ingredient:
        if i in dislike_ingredient:
            if dislike_ingredient[i] >= like_ingredient[i]:
                like_ingredient[i] = 0

    # keep > 0
    onepizza_ingredient = []
    for skey, svalue in like_ingredient.items():
        if svalue>0:
            onepizza_ingredient.append(skey)
    #print(onepizza_ingredient)
    outputfile(fileout, onepizza_ingredient)


def readfile(filein):

    f = open(filein, "r")

    # split line 1
    clients_count = int(f.readline())

    # clients (list of Client)
    clients = []
    for c in range(clients_count):
        array_like = f.readline().split()
        array_dislike = f.readline().split()
        clients.append(Client((array_like[1:]), array_dislike[1:]))

    f.close()
    return clients


def outputfile(fileout, onepizza_ingredient):

    print(f"Write output in: {fileout}")
    fout = open(fileout, "w")
    fout.write(str(len(onepizza_ingredient))+' '+" ".join(onepizza_ingredient))
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