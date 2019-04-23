import logging
import os

from src.gui import Application

if __name__ == '__main__':
    os.remove('output.log')
    logging.basicConfig(filename='output.log',
                        format='%(asctime)s [%(levelname)s]: %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S',
                        level=logging.DEBUG)
    logging.info("Start App")
    app = Application()
    app.start()
