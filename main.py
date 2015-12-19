# -*- coding: utf-8 -*-
'''
OctoDog Web Application
Main Web Function
#TODO-change url name 
http://projboard.sinaapp.com/
@author: bambooom
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import URL
from dbhandler import *
from draw3d import draw3d

CREDS_FILE = 'plotly-creds.sec'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OctoDogkey'
app.config.from_object(__name__)
 
reponame_list = fetch_repos()

#def update_list():
#	'''
#	update the name list of repository
#	'''
#	global reponame_list
#	reponame_list = fetch_name_list(fetch_repos_table())
#	return reponame_list

def get_owner_repo_name(repo_url):
	'''
	Parse the url of the repository to get the name of owner and repo.
	'''
	from urlparse import urlparse, urlsplit
	foo = urlparse(repo_url)
	temp_list = foo.path.split('/')
	return temp_list[1], temp_list[2]


@app.route('/', methods=['GET'])
def index():
	global reponame_list
	reponame_list = fetch_repos()
	return render_template("index.html", repos=reponame_list)


class InsertPro(Form):
	repo_url = StringField("Add your project", validators=[URL(
		message='Sorry, this is not a valid URL')])
	submit = SubmitField('Submit')


@app.route('/addpro', methods=['POST','GET'])
def insert_pro():
	'''
	input url of repository and one click to add 
	and redirect to new repository page
	'''
	form = InsertPro()
	global reponame_list
	from get_repos_stats import fetch_for_one
	if form.validate_on_submit():
		session['repo_url'] = form.repo_url.data
		url = session.get('repo_url')
		ownername, reponame = get_owner_repo_name(url)
		repo_stats = fetch_for_one(ownername, reponame)
		new_repo = {'name':reponame, 'url':url, 'owner':ownername, 'stats':repo_stats}
		add_repo(new_repo) # insert into kvdb 
		reponame_list = fetch_repos()
		return redirect(url_for('show_pro', reponame=reponame, 
			repos=reponame_list, _external=True))	
	return render_template("project.html", repos=reponame_list, 
		form=form, repo_url=session.get('repo_url'))

@app.route('/delpro')
def doDelete():
	kv = sae.kvdb.Client()
	temp = kv.getkeys_by_prefix("repo#")
	for i in temp:
		kv.delete(i)

@app.route('/project/<reponame>', methods=['GET'])
def show_pro(reponame):
	# show the project profile with info
	global reponame_list
	reponame_list = fetch_repos()
	ownername = fetch_owner_by_repo(reponame)
	return render_template("profile.html", reponame=reponame, 
		repos=reponame_list, ownername=ownername)
	#return 'showcase for project %s' % reponame

@app.route('/about', methods=['GET'])
def about_us():
	# post README here
	global reponame_list
	reponame_list = fetch_repos()
	return render_template("about.html", repos=reponame_list)

@app.route('/tools', methods=['GET'])
def tools():
	# show toolbox here
	global reponame_list
	reponame_list = fetch_repos()
	return render_template("tools.html", repos=reponame_list)

@app.route('/rank', methods=['GET'])
def ranks():
	# show toolbox here
	global reponame_list
	reponame_list = fetch_repos()

	import plotly.plotly as py
	creds=[]
	with open(app.config['CREDS_FILE']) as f:
		creds = [x.strip('\n') for x in f.readlines()]

	res = py.sign_in(creds[0],creds[1])
	get_graph_data(fetch_repo_dict())

	import sae.kvdb
	kv = sae.kvdb.Client()
	graph_data = kv.get("graph")
	ploturl=draw3d(graph_data)
	kv.disconnect_all()

	return render_template("rank.html", repos=reponame_list, ploturl=ploturl)

@app.route('/cron', methods=['GET'])
def cron_update():
	repo_dict_list = fetch_repo_dict()
	for repo in repo_dict_list:
		update_stats(repo)
	
	repo_dict_list = fetch_repo_dict()
	get_graph_data(repo_dict_list)

if __name__ == '__main__':
	app.run(debug=True)