# -*- coding: utf-8 -*-

import sae
from board import app

application = sae.create_wsgi_app(app)
