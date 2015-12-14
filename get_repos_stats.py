# -*- coding: utf-8 -*-
'''
list stats data for the given repos.
@author: hysic
'''

import requests

auth = ("octodog-auth", "octoocto2015")

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
        r = requests.get(next_url, auth=auth)
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
    r2 = requests.get(url2, auth=auth)

    if r2.status_code == 200:
        repo_data = r2.json()
        stars_count = repo_data["stargazers_count"]
        watchers_count = repo_data["watchers_count"]
        forks_count = repo_data["forks_count"]
    else:
        return None

    # return a set of the commits/stars/watchers/forks count
    return stars_count+watchers_count+forks_count

def get_contributors_commits(owner, repo):
    '''
    get the commits count of each contributor.
    '''
    url3 = url+"/repos/"+owner+"/"+repo+"/stats/contributors"
    r3 = requests.get(url3, auth=auth)
    contributors = {}

    for people in r3.json():
        name = people["author"]["login"]
        commits_count = people["total"]
        contributors[name] = commits_count

    return contributors

def compute_uneven(owner, repos):
    tmp = get_contributors_commits(owner, repos)
    tmp2 = [tmp[name] for name in list(tmp)]
    return round((max(tmp2)-min(tmp2))*len(tmp2)/float(sum(tmp2)),2)

def fetch_stat():
    #repo_dict = {'Run-map': 'RUNMAP'}
    repo_dict = read_repos()
    results_list = []
    for owner, repo in repo_dict.items():
        repo_stats_dict = {}
        repo_stats_dict["name"] = repo
        repo_stats_dict["commits"] = get_commits_count(owner, repo)
        repo_stats_dict["attention"] = get_repo_stats(owner, repo)
        repo_stats_dict["uneven"] = compute_uneven(owner, repo)
        results_list.append(repo_stats_dict)

    return results_list

if __name__ == "__main__":
    print fetch_stat()
