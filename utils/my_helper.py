# -*- coding: utf-8 -*-
__author__ = 'sunary'


def not_null(field_value):
    if field_value == 0 or field_value == False:
        return True
    return field_value

def pandas_null(content):
    return str(content).lower() == 'nan' or not content

def except_pandas_value(content):
    if pandas_null(content):
        return ' '
    return content

def dataframe_same_length(dataframe, fields):
    max_len = 0
    for f in fields:
        if max_len < len(dataframe[f]):
            max_len = len(dataframe[f])
    for f in fields:
        for i in range(max_len - len(dataframe[f])):
            dataframe[f].append(' ')

    return dataframe

def get_dataframe_columns(file_path, sep=','):
    with open(file_path, 'r') as fo:
        columns = fo.readline().replace('\n', '').replace('\r', '').split(sep)

    columns = [f[1:-1] if ((f.startswith('\'') and f.endswith('\'')) or (f.startswith('"') and f.endswith('"'))) else f for f in columns]

    for i in range(len(columns)):
        if columns[i] == '' or columns[i] == ' ':
            return columns[:i]
    return columns

def len_dataframe(file_path):
    num_row = -1
    with open(file_path, 'r') as fo:
        while fo.readline():
            num_row += 1

    return num_row

def check_exist_url(url):
    import requests

    try:
        res = requests.get(url)
        return (res.status_code == 200)
    except:
        return False

def get_redirected_url(url):
    import urllib2

    try:
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
        request = opener.open(url)
        return request.url
    except:
        return ''

def init_logger(name, log_level=None, log_file=None):
    import logging
    import logging.handlers

    logger = logging.getLogger(name)
    if log_level:
        logger.setLevel(log_level)
    else:
        logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    if log_file:
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=2 * 1024 * 1024, backupCount=3)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def subprocess_output(command, cwd=None):
    import subprocess

    process = subprocess.Popen(command,
                                cwd=cwd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    output_str = ''
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_str += '\n' + output.strip()

    return output_str

def bson2json(row):
    from bson import ObjectId
    from datetime import datetime

    if isinstance(row, dict):
        for k in row:
            if isinstance(row[k], ObjectId):
                row[k] = unicode(row[k])
            elif isinstance(row[k], datetime):
                row[k] = row[k].isoformat()
            elif isinstance(row[k], (dict, list)):
                bson2json(row[k])
    elif isinstance(row, list):
        for i in range(len(row)):
            if isinstance(row[i], ObjectId):
                row[i] = unicode(row[i])
            elif isinstance(row[i], datetime):
                row[i] = row[i].isoformat()
            elif isinstance(row[i], dict):
                bson2json(row[i])

def flatten_dict(deep_dict, parent_key='', sep='.'):
    '''
    Examples:
        >>> flatten_dict({'1': {'3': 'a'}, '2': {'4': 'b'}})
        {'2.4': 'b', '1.3': 'a'}
    '''
    flatten = []
    for key, value in deep_dict.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            flatten.extend(flatten_dict(value, new_key, sep).items())
        else:
            flatten.append((new_key, value))

    return dict(flatten)

def csv_to_xlsl(file_csv, file_xlsx):
    import csv
    from xlsxwriter.workbook import Workbook

    if file_xlsx is None:
        file_xlsx = file_csv + '.xlsx'

    workbook = Workbook(file_xlsx)
    worksheet = workbook.add_worksheet()
    fo = open(file_csv, 'rb')
    reader = csv.reader(fo)
    for r, row in enumerate(reader):
        for c, col in enumerate(row):
            worksheet.write(r, c, col)
    fo.close()
    workbook.close()


if __name__ == '__main__':
    import doctest
    doctest.testmod()