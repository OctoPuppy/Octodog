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
    temp1 = [i[1] for i in list(kv.get_by_prefix("repo@"))]
    temp2 = sorted(temp1, key = lambda x:x['name'])
    name_list = [temp2[i]['name'] for i in range(len(temp2))]
    kv.disconnect_all()
    return name_list

def fetch_repo_dict():
    kv = sae.kvdb.Client()
    temp = [i[1] for i in kv.get_by_prefix("repo@")]
    kv.disconnect_all()
    return temp

def fetch_owner_by_repo(repo):
    temp = fetch_repo_dict()
    for i in temp:
        if i["name"] == repo:
            return i["owner"]
    return None

def add_repo(new_repo):
    kv = sae.kvdb.Client()
    key = "repo@" + str(new_repo['name'])
    kv.set(key,new_repo)
    kv.disconnect_all()

def get_graph_data(repo_dict):
    namelist=[]
    cmlist=[]
    attlist=[]
    uelist=[]
    for repo in repo_dict:
        for key, value in repo.items():
            if key == "name":
                namelist.append(value)
            elif key == "stats":
                cmlist.append(value[0])
                attlist.append(value[1])
                uelist.append(value[2])
    data = [namelist,cmlist,attlist,uelist]
    kv=sae.kvdb.Client()
    kv.set("graph",data)
    kv.disconnect_all()

def get_table_data(repo_dict):
    table_data=[]
    for repo in repo_dict:
        tdict={}
        for key, value in repo.items():
            if key == "name":
                tdic[key]=value
            elif key == "stats":
                tdic["commits"]=value[0]
                tdic["attention"]=value[1]
                tdic["uneven"]=value[2]
        table_data.append(tdic)

    kv=sae.kvdb.Client()
    kv.set("table", table_data)
    kv.disconnect_all()

def update_stats(repo):
    kv=sae.kvdb.Client()
    key = "repo@" + str(repo['name'])
    
    from get_repos_stats import fetch_for_one
    repo['stats'] = fetch_for_one(repo['owner'],repo['name'])
    kv.set(key, repo)
    kv.disconnect_all()


#new_repo=('OctoDog','https://github.com/OctoPuppy/Octodog')
#add_repo(new_repo)
#add_repo(new_repo)
#add_repo(new_repo)
#reponame_list = fetch_name_list(fetch_repos_table())
#print reponame_list
#a = get_repo_table()

#print len(a)