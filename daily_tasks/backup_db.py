import argparse
import sqlite3
import shutil
import time
import os

def sqlite3_backup(dbfile, backupdir):
    """Create timestamped database copy"""

    if not os.path.isdir(backupdir):
        raise Exception("Backup directory does not exist: {}".format(backupdir))

    backup_file = os.path.join(backupdir, os.path.basename(dbfile) +
                               time.strftime("_%Y%m%d_%H%M%S"))

    connection = sqlite3.connect(dbfile)
    cursor = connection.cursor()

    # Lock database before making a backup
    # cursor.execute('begin immediate')
    # Make new backup file
    shutil.copyfile(dbfile, backup_file)
    print ("\nCreating {}...".format(backup_file))
    # Unlock database
    # connection.rollback()

def clean_data(backup_dir):
    """Delete files older than NO_OF_DAYS days"""
    # How old a file needs to be in order
    # to be considered for being removed
    NO_OF_DAYS = 14

    print ("\n------------------------------")
    print ("Cleaning up old backups")

    for filename in os.listdir(backup_dir):
        backup_file = os.path.join(backup_dir, filename)
        if os.path.isfile(backup_file):
            if os.stat(backup_file).st_ctime < (time.time() - NO_OF_DAYS * 86400):
                os.remove(backup_file)
                print ("Deleting {}...".format(backup_file))

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'lost_found')
    os.chdir(path)
    dbfile = 'db.sqlite3'
    backupdir = os.path.join(os.getcwd(), 'db_backups')
    sqlite3_backup(dbfile, backupdir)
    clean_data(backupdir)
