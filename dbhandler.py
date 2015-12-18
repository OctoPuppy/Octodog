# -*- coding: utf-8 -*-
'''
OctoDog Web Application
Database
http://projboard.sinaapp.com/
@author: bambooom
'''

import sae.kvdb
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#ROOT = os.path.dirname(os.path.abspath(__file__))

def fetch_repos():
    kv = sae.kvdb.Client()
    temp1 = [i[1] for i in list(kv.get_by_prefix("repo#"))]
    temp2 = sorted(temp1, key = lambda x:x['name'])
    name_list = [temp2[i]['name'] for i in range(len(temp2))]
    kv.disconnect_all()
    return name_list

def fetch_owner_by_repo(repo):
    kv = sae.kvdb.Client()
    temp = [i[1] for i in kv.get_by_prefix("repo#")]
    kv.disconnect_all()
    for i in temp:
        if i["name"] == repo:
            return i["owner"]
    return None

    #conn = sqlite3.connect(ROOT + '/Repository.db')
    #c = conn.cursor()
    #c.execute('CREATE TABLE if not exists repos (reponame text, repourl text)')
    #c.execute('CREATE UNIQUE INDEX if not exists id ON repos (reponame, repourl)')
    #c.execute('SELECT * FROM repos')
    #repos_table = [list(e) for e in c.fetchall()]
    #return repos_table
    
#def fetch_name_list(repos_table):
#   name_list = [repos_table[i][0] for i in range(len(repos_table))]
#    return name_list

def add_repo(new_repo):
    kv = sae.kvdb.Client()
    key = "repo#" + str(len(fetch_repos()))
    kv.set(key,new_repo)
    kv.disconnect_all()



    #conn = sqlite3.connect(ROOT + '/Repository.db')
    #c = conn.cursor()
    #c.execute('CREATE TABLE if not exists repos (reponame text, repourl text)')
    #c.execute('INSERT OR IGNORE INTO repos VALUES (?,?)', new_repo) 
    # INSERT OR IGNORE to ignore the duplicate value input
    #conn.commit()
    #conn.close()

#new_repo=('OctoDog','https://github.com/OctoPuppy/Octodog')
#add_repo(new_repo)
#add_repo(new_repo)
#add_repo(new_repo)
#reponame_list = fetch_name_list(fetch_repos_table())
#print reponame_list
#a = get_repo_table()

#print len(a)