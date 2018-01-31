import os
import backup_db
import clean_logs






if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'lost_found')
    os.chdir(path)
    dbfile = 'db.sqlite3'
    backupdir = os.path.join(os.getcwd(), 'db_backups')
    backup_db.sqlite3_backup(dbfile, backupdir)
    backup_db.clean_data(backupdir)

    logs_dir = os.path.join(os.getcwd(), 'logs')
    clean_logs.clean_logs(logs_dir)