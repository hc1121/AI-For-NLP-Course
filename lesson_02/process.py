import os
from hanziconv import HanziConv
import re


def get_path(root_path):
    ALL = []
    for root, dirs, files in os.walk(root_path):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        for file in files:
            ALL.append(os.path.join(root, file))
    return ALL


def qu_kong(list):
    return [l for l in list if l != []]


def get_text_from_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        t = f.read()
    t = t.split('</doc>')  # 将文档中的每篇文章先分开来

    for ele in t:
        k = re.findall('title="(.*)"', ele)  # 读取每篇文章title
        try:
            if k != []:
                f = ele.split('title="%s">\n' % (k[0]))  # 根据title切分每篇文章内容，
                want = f[1].strip()  # 获得每篇文章的正文
                want = re.sub('\n+', ' ', want)  # 将每篇正文中的换行符转化成空格，让每一行代表一篇文章
                want = ' '.join(re.findall('[\w|\d]+', want))  # 去标点及特殊字符
                # print(want)
                want = HanziConv.toSimplified(want)  # 繁转简
                with open('text', 'a', encoding='utf-8') as o:
                    o.write(want)
                    o.write('\n')
        except Exception as e:
            print(html_path)
            print(ele)
            print(k)
            continue


if __name__ == '__main__':
    root_path = 'G:\AI_FOR_NLP\wikiextractor\wiki'
    all_path = qu_kong(get_path(root_path))
    for path in all_path:
        get_text_from_html(path)

    with open('text', 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f]

    twentyth_of_size = len(texts) // 20
    twentyth_text = texts[:twentyth_of_size] #取5%的文章
    with open('twentyth_text', 'a', encoding='utf-8') as o:
        # 5%文章合成一个字符串的形式保存
        for line in twentyth_text:
            line = line.strip()
            o.write(line + ' ')
