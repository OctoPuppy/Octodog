# -*- coding: utf-8 -*-
'''
ProjectBoard Web Application
Access http://projboard.sinaapp.com/
@author: bambooom
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, request, redirect, url_for, flash
import sae
import sae.kvdb
from time import localtime, strftime

app = Flask(__name__)
kv = sae.kvdb.Client()

# key for each group = 1pro, 2pro....

def load_comment():
	log = []
	for i in list(kv.get_by_prefix('pr')):
		log.append(i[1])
	return log

def input_comment(new_comment,count):
	countkey = "pr" + str(count)
	comment_time = strftime("%Y %b %d %H:%M", localtime())
	comments = {'time':comment_time,'comment':new_comment}
	kv.set(countkey,comments)

@app.route('/')
def board():
	comment_log = load_comment()
	return render_template("projboard.html", comment_log=comment_log)

@app.route('/', methods=['POST'])
def leave_comment():
	count = len(load_comment())
	new_comment = unicode(request.forms['newcomment'],'utf-8')

	input_comment(new_comment,count)
	comment_log = load_comment()
	return redirect(url_for('projboard'))

#@app.route('/', method='DELETE')
#def delete():
#	temp = kv.getkeys_by_prefix("key#")
#	for i in temp:
#		kv.delete(i)

if __name__ == '__main__':
	app.run()