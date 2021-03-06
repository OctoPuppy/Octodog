# -*- coding: utf-8 -*-
'''
list stats data for the given repos.
@author: hysic
'''

import requests
from multiprocessing.dummy import Pool as ThreadPool

auth = ("octodog-auth", "octoocto2015")

repotext = [
"https://github.com/yondjune/iMatch",
"https://github.com/Run-map/RUNMAP",
"https://github.com/Wangqiaoyang/RIA-Database",
"https://github.com/sherlockhoatszx/Stock_Pickup_and_Reminding",
"https://github.com/penguinjing/PhotoxOrganizer",
"https://github.com/ivanlau/jizhemai",
"https://github.com/imoodmap/imoodmapGroup",
"https://github.com/xpgeng/straypetshelper",
"https://github.com/liangchaob/whenmgone",
"https://github.com/junjielizero/Hunting-for-Great-Books",
"https://github.com/liangpeili/housebuy",
"https://github.com/OctoPuppy/Octodog",
"https://github.com/wp-lai/mipe",
"https://github.com/Cen74/less-habit"
]

def read_repos():
    '''
    load all the repos url to a dict
    key = owner_name, value = repo_name
    '''
    repo_dict = {}
    for item in repotext:
        temp_list = item.split('/')
        owner = temp_list[-2]
        repo = temp_list[-1]
        repo_dict[owner] = repo

    return repo_dict

def fetch_repo_by_owner(owner):
    temp = read_repos()
    return temp[owner]

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
        watchers_count = repo_data["subscribers_count"]
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

def compute_uneven(owner, repo):
    tmp = get_contributors_commits(owner, repo)
    tmp2 = [tmp[name] for name in list(tmp)]
    if tmp2:
        tmp2 = tmp2
    else:
        return 0
    return round((max(tmp2)-min(tmp2))*len(tmp2)/float(sum(tmp2)),2)

def fetch_for_one(owner, repo):
    #repo = fetch_repo_by_owner(owner)
    x = get_commits_count(owner, repo) # commits number
    y = get_repo_stats(owner, repo) # attention=watch+star+fork
    z = compute_uneven(owner, repo)
    coordinate = [x, y, z]
    return coordinate


#def fetch_stat():
    #repo_dict = {'Run-map': 'RUNMAP'}
#    repo_dict = read_repos()
#    results_list = []
#    for owner, repo in repo_dict.items():
#        repo_stats_dict = {}
#        repo_stats_dict["name"] = repo
#        repo_stats_dict["commits"] = get_commits_count(owner, repo)
#        repo_stats_dict["attention"] = get_repo_stats(owner, repo)
#        repo_stats_dict["uneven"] = compute_uneven(owner, repo)
#        results_list.append(repo_stats_dict)

#    return results_list

# if __name__ == "__main__":
#     import time 
#     start = time.time()
#     repo_dict = read_repos()
#     result = {}
#     for owner, repo in repo_dict.items():
#         result[owner] = fetch_for_one(owner, repo)
#     print result
#     end = time.time()
#     print "Time: %d" % (end - start)
# >>> "TIme: 87"

if __name__ == "__main__":
    import time 
    start = time.time()
    owners = read_repos().keys()

    pool = ThreadPool(8)
    result = pool.map(fetch_for_one, owners)
    pool.close() 
    pool.join() 

    print owners
    print result

    end = time.time()
    print "Time using ThreadPool: %d" % (end - start)