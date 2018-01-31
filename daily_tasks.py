import os
import backup_db






if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'lost_found')
    os.chdir(path)
    dbfile = 'db.sqlite3'
    backupdir = os.path.join(os.getcwd(), 'db_backups')
    backup_db.sqlite3_backup(dbfile, backupdir)
    backup_db.clean_data(backupdir)