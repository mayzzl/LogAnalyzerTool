import pandas as pd
from config.cfg import LOG_FILE
from itertools import takewhile, repeat


def iter_count(file_name):
    """
    性能/统计log文件行数
    :param file_name:
    :return:
    """
    buffer = 1024 * 1024
    with open(file_name, 'r', encoding='utf-8') as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)


def log_load(file_name):
    """
    加载不同格式log文件(.txt/.log)，考虑文件大小
    :param file: log文件
    :return: log
    """
    with open(file_name, 'r', encoding='utf-8') as log_file:
        cnt = 1
        for line in log_file:
            print(line)
            cnt += 1
            if cnt == 100:
                break


def keyword_load(file_name, type):
    """
    加载关键字表(.xls/.csv)
    :param file: 关键字表
    :return: keyword
    """
    if type == 'csv':
        return pd.read_csv(file_name)
    elif type == 'xlsx':
        return pd.read_excel(file_name)
    else:
        return open(file_name, 'r', encoding='utf-8')


if __name__ == '__main__':
    line_count = iter_count(LOG_FILE)
