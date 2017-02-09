# publish
pushlish your site／dir to cloud

之前只支持上传到qiniu.com

# install
`pip install publish2cloud`

# config
默认配置文件为"~/.publish.yml" (自行创建)

```yaml
QINIU_ACCESS_KEY: xxx
QINIU_SECRET_KEY: xx
QINIU_BUCKET: xxx
QINIU_BUCKET_DOMAIN: xxx.xxx.clouddn.com
```

# usage
```
#help
publish -h
# publish your site/dir
publish dir_path
```
