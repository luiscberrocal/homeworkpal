import datetime
import os
import shutil

__author__ = 'LBerrocal'


def filename_with_datetime(file_path, base_filename):
    '''
    os.path.join(TEST_OUTPUT_PATH, '%s_%s.xlsx' % ('maximo_tickets', timezone.now().strftime('%Y%m%d_%H%M')))
    :param file_path:
    :param base_filename:
    :return:
    '''
    parts = base_filename.split('.')
    if len(parts) > 2:
        raise ValueError('Base filename cannot contain more the one dot')
    str_date = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    return os.path.join(file_path, '%s_%s.%s' % (parts[0], str_date, parts[1]))

if __name__ == '__main__':
    source = r'C:\Users\lberrocal\PycharmProjects\homeworkpal\homeworkpal_project\homeworkpal_project\homework_pal.sqlite3'
    _, base_filename = os.path.split(source)
    backup_paths = [r'F:\backup_homeworkpal', r'C:\Users\lberrocal\OneDrive - Autoridad del Canal de Panama\2016_Project_admin']
    for b_path in backup_paths:
        if os.path.exists(b_path):
            target_filename = filename_with_datetime(b_path, base_filename)
            shutil.copy(source, target_filename)
            print('Backup to %s' % target_filename)