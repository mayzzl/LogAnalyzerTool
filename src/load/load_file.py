# -*- coding: utf-8 -*-
import pandas as pd


def load_file():
    modules = []
    types = []
    keywords = []
    reason = []

    df0 = pd.read_excel('../../docs/keywords.xlsx', usecols=[0], names=None)
    df1 = pd.read_excel("../../docs/keywords.xlsx", usecols=[1], names=None)
    df2 = pd.read_excel("../../docs/keywords.xlsx", usecols=[2], names=None)
    df3 = pd.read_excel("../../docs/keywords.xlsx", usecols=[3], names=None)

    df_li0 = df0.values.tolist()
    df_li1 = df1.values.tolist()
    df_li2 = df2.values.tolist()
    df_li3 = df3.values.tolist()

    for s_li0 in df_li0:
        modules.append(s_li0[0])
    for s_li1 in df_li1:
        types.append(s_li1[0])
    for s_li2 in df_li2:
        keywords.append(s_li2[0])
    for s_li3 in df_li3:
        reason.append(s_li3[0])

    return modules, types, keywords, reason


if __name__ == '__main__':
    load_file()
