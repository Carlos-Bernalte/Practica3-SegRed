#!/usr/bin/env python3
import argparse
from src.config import APP_HOST, APP_PORT, APP_DEBUG
from src.app import app

argparser = argparse.ArgumentParser()
argparser.add_argument('--host', default=APP_HOST)
argparser.add_argument('--port', default=APP_PORT)
args = argparser.parse_args()

context = ('./cert/cert.pem', './cert/key.pem')
app.run(debug=APP_DEBUG, host=args.host, port=args.port, ssl_context=context)

