# -*- coding: utf-8 -*-
'''
OctoDog Web Application
Main Web Function
http://octodog.sinaapp.com/
@author: bambooom
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sae.kvdb
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import URL
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from flaskext.markdown import Markdown
from dbhandler import *
from draw3d import draw3d

CREDS_FILE = 'plotly-creds.sec'

app = Flask(__name__)
pagedown = PageDown(app)
Markdown(app)
app.config['SECRET_KEY'] = 'OctoDogkey'
app.config.from_object(__name__)
 
reponame_list = fetch_repos()

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
		return redirect(url_for('show_pro', reponame=reponame))	
	return render_template("addpro.html", repos=reponame_list, 
		form=form, repo_url=session.get('repo_url'))

@app.route('/deleteall') #TODO: delete repository one by one
def delete_all():
	'''
	delete all repository
	'''
	kv = sae.kvdb.Client()
	temp = kv.getkeys_by_prefix("repo#")
	for i in temp:
		kv.delete(i)
	return redirect(url_for('index'))

@app.route('/delete')
def delete_page():
	'''
	delete project page
	'''
	global reponame_list
	reponame_list = fetch_repos()
	return render_template("delete.html", repos=reponame_list)

@app.route('/delete/<reponame>')
def delete_pro(reponame):
	'''
	delete one repo data
	'''
	kv = sae.kvdb.Client()
	key = "repo#"+str(reponame)
	kv.delete(key)
	kv.disconnect_all()
	return redirect(url_for('delete_page'))

#class PageDownForm(Form):
#    pagedown = PageDownField('Edit Content')
#    submit = SubmitField('Submit')

@app.route('/project/<reponame>', methods=['GET'])
def show_pro(reponame):
	'''
	show the project profile with info
	'''
	global reponame_list
	reponame_list = fetch_repos()
	ownername = fetch_owner_by_repo(reponame)
	kv = sae.kvdb.Client()
	repo_content = kv.get(str(reponame))
	kv.disconnect_all()
	return render_template("profile.html", reponame=reponame, 
		repos=reponame_list, ownername=ownername, content=repo_content)
	#return 'showcase for project %s' % reponame

@app.route('/project/<reponame>/edit', methods=['POST'])
def edit_pro(reponame):
	global reponame_list
	reponame_list = fetch_repos()
	kv = sae.kvdb.Client()
	content = "\n" + request.form["editContent"] # bugs for flask-markdown, need /n
	kv.set(str(reponame), content)
	return redirect(url_for('show_pro', reponame=str(reponame)))


@app.route('/about', methods=['GET'])
def about():
	'''
	about OctoDog page
	'''
	global reponame_list
	reponame_list = fetch_repos()

	kv = sae.kvdb.Client()
	about_content = kv.get('about')
	kv.disconnect_all()
	return render_template("info.html", title="ABOUT", page="about", 
		repos=reponame_list, content=about_content)

@app.route('/<page>/edit', methods=['POST'])
def edit_mode(page):
	'''
	Edit in markdown and 
	save it to see markdown in html
	'''
	global reponame_list
	reponame_list = fetch_repos()

	#if 'project' in str(page).split('/'):
	#	pagename = str(page).split('/')[-1]
	#else:
	#	pagename = str(page)

	kv = sae.kvdb.Client()
	content = "\n" + request.form["editContent"] # bugs for flask-markdown, need /n
	kv.set(str(page), content)
	#if 'project' in str(page).split('/'):
	#	return redirect(url_for('show_pro', reponame=pagename))
	#else:
	return redirect(url_for(str(page)))
	#form = PageDownForm()
	#if form.validate_on_submit():
	#	page_content = "\n"+form.pagedown.data
	#	kv.set(pagename, page_content)
	#	kv.disconnect_all()
	#	if 'project' in str(page).split('/'):
	#		return redirect(url_for('show_pro', reponame=pagename))
	#	else:
	#		return redirect(url_for(pagename))

	#form.pagedown.data = kv.get(pagename)
	#kv.disconnect_all()
	#return render_template('edit_mode.html', title=pagename.upper(),
	#	repos=reponame_list, form=form)

@app.route('/tools', methods=['GET'])
def tools():
	'''
	show toolbox here
	'''
	global reponame_list
	reponame_list = fetch_repos()
	kv = sae.kvdb.Client()
	tools_content = kv.get('tools')
	kv.disconnect_all()
	return render_template("info.html", title="TOOLS", page="tools",
		repos=reponame_list, content=tools_content)

@app.route('/rank/table.html', methods=['GET'])
def table():
	'''
	sortable table, only for display on /rank page
	'''
	get_table_data(fetch_repo_dict())
	kv = sae.kvdb.Client()
	table_data = kv.get("table")
	kv.disconnect_all()
	return render_template("table.html", table_data=table_data)


@app.route('/rank', methods=['GET'])
def rank():
	'''
	Rank methodology & measurement
	Data table sortable
	3D plot of rank
	'''
	global reponame_list
	reponame_list = fetch_repos()

	import plotly.plotly as py
	creds=[]
	with open(app.config['CREDS_FILE']) as f:
		creds = [x.strip('\n') for x in f.readlines()]

	res = py.sign_in(creds[0],creds[1])
	get_graph_data(fetch_repo_dict())

	kv = sae.kvdb.Client()
	wiki_content = kv.get('rank')
	graph_data = kv.get("graph")
	ploturl=draw3d(graph_data)
	kv.disconnect_all()

	return render_template("rank.html", repos=reponame_list, title="RANK", 
		page="rank", content=wiki_content, ploturl=ploturl)

@app.route('/cron', methods=['GET'])
def cron_update():
	#from multiprocessing.dummy import Pool as ThreadPool

	repo_dict_list = fetch_repo_dict()
	#pool = ThreadPool(8)
	#pool.map(update_stats, repo_dict_list)
	#pool.close()
	#pool.join()

	for repo in repo_dict_list:
		update_stats(repo)
	
	repo_dict_list = fetch_repo_dict()
	get_graph_data(repo_dict_list)
	return "Update Data Successfully"

if __name__ == '__main__':
	app.run(debug=True)