# -*- coding: utf-8 -*-
'''
list stats data for the given repos.
@author: hysic
'''

import requests

# load all the repos in the dict
# key = owner_name, value = repo_name
repo_dict = {}
with open("repos.txt", "r") as f:
    for line in f:
        temp_list = line.strip('\n').split('/')
        owner = temp_list[-2]
        repo = temp_list[-1]
        repo_dict[owner] = repo

url = "https://api.github.com"
#auth = (username, password)

for owner in repo_dict:
    repo = repo_dict[owner]
    print "In " +owner+"/"+repo

    # get the contributor number, and their respective commits number.
    # This commits number is consistent with the number in pulse page, 
    # but is not consistent with the number in the homepage,
    # becouse it does not inclue the merged commits.
    url1 = url+"/repos/"+owner+"/"+repo+"/stats/contributors"
    r1 = requests.get(url1)
    if r1.status_code == 200:
        contributor_data = r1.json()
        contributor_num = len(contributor_data)
        print "There are %d contributors, their commits number are as follows:" % contributor_num
        for people in contributor_data:
           print people["author"]["login"]+":"+str(people["total"])
    else:
        print "Wrong status_code:" + str(r1.status_code)

    # get the commits number consistent with the number in homepage.
    # r2 = requests.get(url+"/repos/"+owner+"/"+repo+"/commits")
    # if r2.status_code == 200:
    #     commits = r2.json()
    #     for commit in commits:
    #         print commit["committer"]["login"]

    # get the star/watch/fork number for a repo
    url2 = url+"/repos/"+owner+"/"+repo
    r2 = requests.get(url2)
    if r2.status_code == 200:
        repo_data = r2.json()
        print "The repo has been stared by %d times, watched by %d times, and forked by %d times." % (repo_data["stargazers_count"], repo_data["watchers_count"], repo_data["forks_count"])
    else:
        print "Wrong status_code:" + str(r2.status_code)

    print
