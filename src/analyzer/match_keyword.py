import re
import numpy as np
import pandas as pd

from src.load.load_file import load_file


def re_match(file_line, key_word):
    res_list = []
    pattern = re.compile(key_word)
    res = pattern.match(file_line)
    print(res)
    if res is not None:
        res_list.append(res)
    return res_list


def post_process(matched_line):
    """
    处理成表的形式
    :risk 因为取的是固定索引分隔，需要求log文件的格式必须按规定生成
    :param matched_line:
    :return:
    """
    split_res = matched_line[:42].split()
    data = [split_res[0], split_res[1], split_res[2], split_res[3],
            split_res[4], split_res[5], matched_line[42:]]
    return data


def analyzer(filename):
    modules, types, keywords, reason = load_file()
    for index in range(len(keywords)):
        with open(filename + '/0-android.log', 'r', errors='ignore') as fi:
            for line in fi:
                if keywords[index] in line:
                    print(line, end="\n")
                    print("可能的原因=======" + reason[index])
                    print("=======end=======")


if __name__ == '__main__':
    match_res = []
    keyword = 'decRet'
    with open('../../docs/0-android.log', 'r', encoding='UTF-8',
              errors='ignore') as file:
        for line in file:
            if keyword in line:
                res = post_process(line)
                match_res.append(res)
        df = pd.DataFrame(np.array(match_res),
                          columns=['Tag', 'Date', 'Time', 'PID', 'TID', 'Level',
                                   'Message'])
        df.to_csv('../../res/match_res.csv', index=False, header=True)
        print('test')
