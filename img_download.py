import urllib.request as urllib
import os
cur_path = os.curdir

def get_img(file):
    f = open(file, 'r+')

    for line in f.readlines():
        print(line)
        line_list = line.split(',')
        zpid = line_list[0]
        url = line_list[1]
        if url == 'None':
            continue
        urllib.urlretrieve(url, f"{cur_path}/imgs/{zpid}.jpg")

    f.close()

if __name__ == '__main__':
    get_img('img.csv')
