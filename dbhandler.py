# -*- coding: utf-8 -*-
'''
OctoDog Web Application
Database
http://projboard.sinaapp.com/
@author: bambooom
'''

import sqlite3
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))

def fetch_repos_table():
    conn = sqlite3.connect(ROOT + '/Repository.db')
    c = conn.cursor()
    c.execute('CREATE TABLE if not exists repos (reponame text, repourl text)')
    c.execute('CREATE UNIQUE INDEX if not exists id ON repos (reponame, repourl)')
    c.execute('SELECT * FROM repos')
    repos_table = [list(e) for e in c.fetchall()]
    return repos_table
    
def fetch_name_list(repos_table):
    name_list = [repos_table[i][0] for i in range(len(repos_table))]
    return name_list

def add_repo(new_repo):
    conn = sqlite3.connect(ROOT + '/Repository.db')
    c = conn.cursor()
    c.execute('CREATE TABLE if not exists repos (reponame text, repourl text)')
    c.execute('INSERT OR IGNORE INTO repos VALUES (?,?)', new_repo) 
    # INSERT OR IGNORE to ignore the duplicate value input
    conn.commit()
    conn.close()

#new_repo=('OctoDog','https://github.com/OctoPuppy')
#add_repo(new_repo)
#add_repo(new_repo)
#add_repo(new_repo)
#reponame_list = fetch_name_list(fetch_repos_table())
#print reponame_list
#a = get_repo_table()

#print len(a)