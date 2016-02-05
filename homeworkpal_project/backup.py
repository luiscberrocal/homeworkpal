import datetime
import os
import shutil

import sys
from dropbox import dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode

from homeworkpal_project.settings.local_acp import DROPBOX_TOKEN

__author__ = 'LBerrocal'


def filename_with_datetime(base_filename):
    '''
    os.path.join(TEST_OUTPUT_PATH, '%s_%s.xlsx' % ('maximo_tickets', timezone.now().strftime('%Y%m%d_%H%M')))
    :param base_filename:
    :return:
    '''
    parts = base_filename.split('.')
    if len(parts) > 2:
        raise ValueError('Base filename cannot contain more the one dot')
    str_date = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    return '%s_%s.%s' % (parts[0], str_date, parts[1])


def upload_to_dropbox(source, target_filename):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    with open(source, 'rb') as f:
        try:
            dbx.files_upload(f, target_filename, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

if __name__ == '__main__':
    source = r'C:\Users\lberrocal\PycharmProjects\homeworkpal\homeworkpal_project\homeworkpal_project\homework_pal.sqlite3'
    _, base_filename = os.path.split(source)
    backup_paths = [r'F:\backup_homeworkpal', r'C:\Users\lberrocal\OneDrive - Autoridad del Canal de Panama\2016_Project_admin']
    dated_filename = filename_with_datetime(base_filename)
    for b_path in backup_paths:
        if os.path.exists(b_path):
            target_filename = os.path.join(b_path, dated_filename)
            shutil.copy(source, target_filename)
            print('Backup to %s' % target_filename)
    upload_to_dropbox(source, '/%s' % dated_filename)
    print('Backup to dropbox %s' % dated_filename)
