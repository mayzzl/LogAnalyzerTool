import os
import shutil
import pandas as pd
import tkinter as tk
from tkinter import filedialog

#传一个路径过来扫描生成文件夹
#def main()
root = tk.Tk()
root.withdraw()
fileName = filedialog.askopenfilename()  # 选择打开什么文件，返回文件
father_path = os.path.abspath(os.path.dirname(fileName)+os.path.sep+".")
print(father_path)

#拷贝到当前选择文件的路径下
shutil.copy2('analyzer.py',father_path)

#读取.py文件，生成.ylog
os.system('python ' + father_path + '\\analyzer.py')
fileReadName = fileName[:-5]
print(fileReadName)

#定义表
modules = []
types = []
keywords = []
reason = []

df0 = pd.read_excel("log分析.xlsx", usecols=[0], names=None) #读取项目名称列，不要列名
df1 = pd.read_excel("log分析.xlsx", usecols=[1], names=None) #读取项目名称列，不要列名
df2 = pd.read_excel("log分析.xlsx", usecols=[2], names=None) #读取项目名称列，不要列名
df3 = pd.read_excel("log分析.xlsx", usecols=[3], names=None) #读取项目名称列，不要列名

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
print(reason)

#分析.log中的关键字
print("=======log分析=======")
for index in range(len(keywords)):
    fi = open(fileReadName+'/0-android.log','r',errors='ignore')
    for line in fi:
        if keywords[index] in line:
            print(line,end="\n")
            print("可能的原因======="+reason[index])
            print("=======end=======")
