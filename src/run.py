#!/usr/bin/env python3

from src.config import APP_HOST, APP_PORT, APP_DEBUG
from src.app import app

context = ('./cert/cert.pem', './cert/key.pem')
app.run(debug=APP_DEBUG, host=APP_HOST, port=APP_PORT, ssl_context=context)

