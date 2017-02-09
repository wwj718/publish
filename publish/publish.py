#!/usr/bin/env python
# encoding: utf-8
'''使用：python upload2qiniu.py SITE_DIR
'''

import sys,os
import yaml
import argparse
from qiniu import Auth, put_file, etag, urlsafe_base64_encode,BucketManager,CdnManager
import qiniu.config
from path import path # 文档参考# https://pythontips.com/2014/01/23/python-101-writing-a-cleanup-script/


#需要填写你的 Access Key 和 Secret Key
#export QINIU_ACCESS_KEY=xxx
#access_key = os.environ["QINIU_ACCESS_KEY"]
#export QINIU_SECRET_KEY=xxx
#secret_key = os.environ["QINIU_SECRET_KEY"]

#要上传的空间
#export QINIU_BUCKET=xxx
#bucket_name = os.environ["QINIU_BUCKET"]

#bucket_domain = os.environ["QINIU_BUCKET_DOMAIN"]

class QiniuClient(object):

    def __init__(self,access_key,secret_key,bucket_name,bucket_domain):
        self.bucket_name = bucket_name
        self.bucket_domain = bucket_domain
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        self.q = q
        self.cdn_manager = CdnManager(q)
        #初始化BucketManager
        self.bucket = BucketManager(q)
        self.file2refresh=[]

    def is_diff(self,key,localfile):
        '''
        比较本地文件与文件文件是否一致
        '''
        ret, info = self.bucket.stat(self.bucket_name, key)
        #print(ret,info)
        hash = ret
        if hash:
            diff = ret['hash'] != etag(localfile) # diff==False，说明文件相同，这个有点绕
            return diff
        else:
            diff = True
            # 不存在hash，说明还没上传过
            return True # 为True，说明文件对比结果为不一致

    def refresh(self,urls):
        #https://github.com/qiniu/python-sdk/blob/master/examples/cdn_manager.py 列出所有上传文件，在七牛中刷新
        refresh_url_result = self.cdn_manager.refresh_urls(urls)
        #print_result(refresh_url_result)


    # 上传整个目录到七牛，保存目录结构（在url中实现，本质上是通过命名）
    def upload(self,key,localfile):
        '''
        key 文件在七牛上的名字，和它的url有关 ，参考：http://qiniu-developer.u.qiniudn.com/docs/v6/api/overview/faq.html
        localfile 本地文件路径
        '''
        # 比对本地文件和云端文件，如果不同则上传
        if self.is_diff(key,localfile):
            token = self.q.upload_token(self.bucket_name, key, 3600)
            ret, info = put_file(token, key, localfile)
            #print(ret,info) # 打印出更新文件以便于在七牛中刷新 : https://portal.qiniu.com/refresh
            url  = 'http://{}/{}'.format(self.bucket_domain, key)
            print("refresh url:",url)
            self.file2refresh.append(url) #全局



#要上传的本地文件夹
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path",help="目录路径")
    parser.add_argument("--config", help="配置文件(默认是~/.publish.yml)")
    args = parser.parse_args()
    if args.config:
        config = yaml.safe_load(open(args.config))
    else:
        config = yaml.safe_load(open(os.path.expanduser("~")+"/.publish.yml"))
    root_dir = args.dir_path#sys.argv[1]
    access_key = config["QINIU_ACCESS_KEY"]
    secret_key = config["QINIU_SECRET_KEY"]
    bucket_name = config["QINIU_BUCKET"]
    bucket_domain = config["QINIU_BUCKET_DOMAIN"]
    #print(config["QINIU_ACCESS_KEY"])
    #print(root_dir)
    client = QiniuClient(access_key,secret_key,bucket_name,bucket_domain)
    #sys.exit()

    d = path(root_dir)
    for i in d.walk():
        if i.isfile():
            #只上传文件
            #from IPython import embed;embed()
            key = str(i.abspath()).replace(str(d.abspath())+"/","") #实际是相对路径
            localfile = str(i)
            client.upload(key,localfile) # 返回需要刷新的文件然后一次性刷新
    if client.file2refresh:
        client.refresh(client.file2refresh)
