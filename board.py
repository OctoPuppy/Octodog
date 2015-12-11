# -*- coding: utf-8 -*-
'''
ProjectBoard Web Application
Access http://projboard.sinaapp.com/
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
#kv = sae.kvdb.Client()


# key for each group = 1pro, 2pro....

#def load_comment():
#	log = []
#	for i in list(kv.get_by_prefix('pr')):
#		log.append(i[1])
#	return log

#def input_comment(new_comment,count):
#	countkey = "pr" + str(count)
#	comment_time = strftime("%Y %b %d %H:%M", localtime())
#	comments = {'time':comment_time,'comment':new_comment}
#	kv.set(countkey,comments)


@app.route('/',methods=['GET'])
def board():
#	comment_log = load_comment()
	return render_template("index.html")

class InsertPro(Form):
	projecturl = StringField('Add your project to OctoDog', validators=[URL(message='\
		Sorry, this is not a valid URL')], default='http://github.com/user/repository')
	submit = SubmitField('Submit')


@app.route('/project', methods=['POST','GET'])
def insertpro():
	form = InsertPro()
	if request.method == 'POST':
		if form.validate_on_submit():
			session['projecturl'] = form.projecturl.data
			return redirect(url_for('insertpro'))
		else:
			return render_template("project.html",form = form,projecturl=session.get('projecturl'))
	
	return render_template("project.html",form = form, projecturl=session.get('projecturl'))



@app.route('/project/<projectname>',methods=['GET'])
def show_project(projectname):
	# show the project profile with info
	#return render_template("projectprofile.html")
	return 'showcase for project %s' % projectname



if __name__ == '__main__':
	app.run(debug=True)