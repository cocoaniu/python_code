import requests
import os
from pathlib import Path
import shutil

base_image_path = 'http://img11.jzsjwk.com/pic/'
dir = os.path.abspath('.')

def download_jpg(image_url, image_localpath):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(image_localpath, 'wb') as f:
            response.raw.deconde_content = True
            shutil.copyfileobj(response.raw, f)
        return True
    else:
        return False

def get_image_url(path_num,name_num):
    imgurl = base_image_path + str(path_num) + '/' + str(name_num) + '.jpg'
    return imgurl

def get_local_path(dir,imgurl):
    filename = os.path.basename(imgurl)
    imgpath = os.path.join(dir, filename)
    return imgpath

while True:
    path_str = input("请输入四位数编号：")
    path_num = int(path_str)
    print("正在下载第 %s 套图" % (path_num));
    # 生成套图保存目录
    image_download_dir = os.path.join(dir, str(path_str))
    if os.path.exists(image_download_dir) == False:
        os.mkdir(image_download_dir)
    # 初始化第一张图片下载路径
    name_count = 1
    imgurl = get_image_url(path_num,name_count)
    # 获得本地保存路径
    imgpath = get_local_path(image_download_dir,imgurl)
    while download_jpg(imgurl, imgpath):
        download_jpg(imgurl, imgpath)
        name_count = name_count + 1
        imgurl = get_image_url(path_num,name_count)
        imgpath = get_local_path(image_download_dir,imgurl)