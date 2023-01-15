#!/usr/bin/env python3
import argparse
from src.config import APP_HOST, APP_PORT
from src.app import run_app


def args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--host', default=APP_HOST, type=str)
    argparser.add_argument('--port', default=APP_PORT, type=int)
    return argparser.parse_args()

    

if __name__ == '__main__':
    args = args()
    run_app(args.host, args.port)