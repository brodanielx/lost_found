import time
import os

def clean_logs(logs_dir):
    """Delete files older than NO_OF_DAYS days"""
    # How old a file needs to be in order
    # to be considered for being removed
    NO_OF_DAYS = 14

    print ("\n------------------------------")
    print ("Cleaning up old logs")

    for filename in os.listdir(logs_dir):
        backup_file = os.path.join(logs_dir, filename)
        if os.path.isfile(backup_file):
            if os.stat(backup_file).st_ctime < (time.time() - NO_OF_DAYS * 86400):
                os.remove(backup_file)
                print ("Deleting {}...".format(backup_file))