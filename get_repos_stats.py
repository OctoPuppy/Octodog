# -*- coding: utf-8 -*-
'''
list stats data for the given repos.
@author: hysic
'''

import requests


def read_repos():
    '''
    load all the repos in the txt file to a dict
    key = owner_name, value = repo_name
    '''
    repo_dict = {}
    with open("repos.txt", "r") as f:
        for line in f:
            temp_list = line.strip('\n').split('/')
            owner = temp_list[-2]
            repo = temp_list[-1]
            repo_dict[owner] = repo

    return repo_dict


url = "https://api.github.com"

def get_commits_count(owner, repo):
    '''
    get the commits count for the given repo.
    This commits number is consistent with the number in the homepage.
    '''
    next_url = url+"/repos/"+owner+"/"+repo+"/commits"
    commits_count = 0

    # the r.json() only display 30 commits in one page
    # so I use the while loop, to count all the commits
    while next_url:
        r = requests.get(next_url)
        commits = r.json()
        commits_count  += len(commits)

        if "next" in r.links:
            next_url = r.links["next"]["url"]
        else:
            next_url = ""

    return commits_count

def get_repo_stats(owner, repo):
    '''
    get the star/watch/fork number for a repo
    '''
    url2 = url+"/repos/"+owner+"/"+repo
    r2 = requests.get(url2)

    if r2.status_code == 200:
        repo_data = r2.json()
        stars_count = repo_data["stargazers_count"]
        watchers_count = repo_data["watchers_count"]
        forks_count = repo_data["forks_count"]
    else:
        return (None, None, None)

    # return a set of the commits/stars/watchers/forks count
    return (stars_count, watchers_count, forks_count)

if __name__ == "__main__":
    repo_dict = read_repos()
    results_list = []

    for owner, repo in repo_dict.items():
        repo_stats_dict = {}
        commits = get_commits_count(owner, repo)
        stars, watchers, forks = get_repo_stats(owner, repo)
        repo_stats_dict["name"] = repo
        repo_stats_dict["commits"] = commits
        repo_stats_dict["stars"] = stars
        repo_stats_dict["watchers"] = watchers
        repo_stats_dict["forks"] = forks
        results_list.append(repo_stats_dict)
        print repo_stats_dict
