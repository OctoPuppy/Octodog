# -*- coding: utf-8 -*-
'''
OctoDog Web Application
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
#import sae.kvdb
#from time import localtime, strftime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'OctoDog key'
repository = ['a','b','c','d']

def get_repo_name(repo_url):
	'''
	Parse the url of the repository to get the name.
	'''
	from urlparse import urlparse, urlsplit
	foo = urlparse(repo_url)
	return foo.path.split('/')[2]


@app.route('/',methods=['GET'])
def board():
	return render_template("index.html", repos = repository)


class InsertPro(Form):
	repo_url = StringField("Add your project", validators=[URL(message='\
		Sorry, this is not a valid URL')])
	submit = SubmitField('Submit')


@app.route('/project', methods=['POST','GET'])
def insert_pro():
	form = InsertPro()
	if form.validate_on_submit():
		session['repo_url'] = form.repo_url.data
		u = session.get('repo_url')
		reponame = get_repo_name(u)
		repository.append(reponame)
		# flash("Added Successfully.")
		return redirect(url_for('show_pro', reponame=reponame, 
			repos=repository, _external=True))	
	return render_template("project.html", repos=repository, 
		form=form, repo_url=session.get('repo_url'))

@app.route('/project/<reponame>', methods=['GET'])
def show_pro(reponame):
	# show the project profile with info
	return render_template("profile.html", reponame=reponame, 
		repos=repository)
	#return 'showcase for project %s' % reponame



if __name__ == '__main__':
	app.run(debug=True)