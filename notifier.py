from terminal_msg import *

import csv
import os



def get_users(csv_file: str):
    if not os.path.exists(csv_file):
        pass