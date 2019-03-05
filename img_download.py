import urllib.request as urllib
import os
cur_path = os.curdir

def get_img(file):
    f = open(file, 'r+')
    count = 0
    for line in f.readlines():
        line_list = line.split(',')
        zpid = line_list[0]
        url = line_list[1]
        urllib.urlretrieve(url, f"{cur_path}/imgs/+{zpid}.jpg")
        count += 1
        if count == 10:
            break
    f.close()

if __name__ == '__main__':
    get_img('img.csv')
