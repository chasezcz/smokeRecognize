import logging
import sys
import os


def init():

    try:
        os.remove('output.log')
    except:
        logging.error("there is no output.log")
    else:
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s]: %(message)s',
            # filename='output.log',
            datefmt='%Y-%m-%d %I:%M:%S',
            level=logging.DEBUG)
        # stdout_handler = logging.StreamHandler(sys.stdout)
        # stdout_handler.setLevel(logging.DEBUG)

        # formatter = logging.Formatter('%(levelname)-s: %(message)s')
        # stdout_handler.setFormatter(formatter)

        # logging.getLogger().addHandler(stdout_handler)
