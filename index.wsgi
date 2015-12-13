# -*- coding: utf-8 -*-
'''
OctoDog Web Application
#TODO-change url name 
http://projboard.sinaapp.com/
@author: bambooom
'''

import sae
sae.add_vendor_dir('3rdParty')

from main import app

application = sae.create_wsgi_app(app)
