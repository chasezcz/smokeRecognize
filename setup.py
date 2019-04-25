import logging as log
import os
import sys

import src.log
from src.gui import Application

if __name__ == '__main__':
    # src.log.init()
    log.basicConfig(
        format='%(asctime)s [%(levelname)s]: %(message)s',
        # filename='output.log',
        datefmt='%Y-%m-%d %I:%M:%S',
        level=log.DEBUG)
    log.info("Start App")
    app = Application()
    app.start()
