# -*- coding: utf-8 -*-

import sae
sae.add_vendor_dir('3rdParty')

from board import app

application = sae.create_wsgi_app(app)
