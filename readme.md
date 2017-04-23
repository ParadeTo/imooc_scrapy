# 安装配置
## mysql下载
https://dev.mysql.com/downloads/installer/

## python3 path 
最好用3.5
/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5

## python豆瓣源
pip install *** -i https://pypi.douban.com/simple/

## virtualenv
以python3创建一个目录

virtualenv -p E:\soft\Python36\python.exe testProject

### vcruntime140.dll缺失
把python3中的该文件拷贝到virtualenv创建的目录下的Scripts下面

## virtualenvwrapper
### 安装
windows: pip install virtualenvwrapper-win

mac: --ignore-installed six

### 设置工作目录
WORKON_HOME
### deactivate
### workon **
### mkvirtualenv --python=path\python.exe project
如果还是报vcruntime140.dll缺失，可用``virtualenv -p E:\soft\Python36\python.exe testProject``创建

## windows下包安装出错
www.lfd.uci.edu/~gohlke/pythonlibs/

# 去重
## md5编码url
## bitmap
比如8个员工记录考勤，可以用一个byte来表示，每个bit表示来或者没来

# 编码
utf8一般作为保存，不定字节 8bit unicode transforming format

unicode一般作为编程，因其用固定的2个字节

python3 全部转化为unicode

u"abc" 表示unicode

window下：
```
s = '我用python' # window下是gb2312 linux下是utf8
s.encode("utf8") # 会出错，s必须是unicode
s.decode("gb2312").encode("utf8") # linux utf8
```
# scrapy windows下
** 安装pywin32 http://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32
** 拷贝Lib\site-packages\pywin32_system32 下的文件到系统的system32下面

# item
## github scrapy-djangoitem

## jobbole article
### 知乎
```
DROP TABLE IF EXISTS `zhihu_question`;
CREATE TABLE `zhihu_question` (
  `zhihu_id` bigint(20) NOT NULL,
  `topics` varchar(255) DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `answer_num` int(11) NOT NULL DEFAULT '0',
  `comments_num` int(11) NOT NULL DEFAULT '0',
  `watch_user_num` int(11) NOT NULL DEFAULT '0',
  `click_num` int(11) NOT NULL DEFAULT '0',
  `crawl_time` datetime NOT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
```
DROP TABLE IF EXISTS `zhihu_answer`;
CREATE TABLE `zhihu_answer` (
  `zhihu_id` bigint(20) NOT NULL,
  `url` varchar(300) NOT NULL,
  `question_id` bigint(20) NOT NULL,
  `author_id` varchar(100) DEFAULT NULL,
  `content` longtext NOT NULL,
  `praise_num` int(11) NOT NULL DEFAULT '0',
  `comments_num` int(11) NOT NULL DEFAULT '0',
  `create_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_time` datetime NOT NULL,
  `crawl_time` datetime NOT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
### jobbole
```
CREATE TABLE `jobbole` (
  `title` varchar(200) NOT NULL DEFAULT '',
  `create_date` date DEFAULT NULL,
  `url` varchar(300) NOT NULL DEFAULT '',
  `url_object_id` varchar(50) NOT NULL DEFAULT '',
  `front_image_url` varchar(300) DEFAULT '',
  `front_image_path` varchar(200) DEFAULT NULL,
  `comment_nums` int(11) DEFAULT '0',
  `fav_nums` int(11) DEFAULT '0',
  `praise_nums` int(11) DEFAULT '0',
  `tags` varchar(200) DEFAULT NULL,
  `content` longtext,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
### lagou
```
DROP TABLE IF EXISTS `lagou_job`;
CREATE TABLE `lagou_job` (
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `title` varchar(100) NOT NULL,
  `salary` varchar(20) DEFAULT NULL,
  `job_city` varchar(10) DEFAULT NULL,
  `work_years` varchar(100) DEFAULT NULL,
  `degree_need` varchar(30) DEFAULT NULL,
  `job_type` varchar(20) DEFAULT NULL,
  `publish_time` varchar(20) NOT NULL,
  `tags` varchar(100) DEFAULT NULL,
  `job_advantage` varchar(1000) DEFAULT NULL,
  `job_desc` longtext NOT NULL,
  `job_addr` varchar(50) DEFAULT NULL,
  `company_url` varchar(300) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `crawl_time` datetime NOT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
### 代理
```
DROP TABLE IF EXISTS `proxy_ip`;
CREATE TABLE `proxy_ip` (
  `ip` varchar(20) NOT NULL,
  `port` varchar(255) NOT NULL,
  `speed` float DEFAULT NULL,
  `proxy_type` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

# 关于SEO友好
非正常页面不要返回200，否则，百度爬虫等会认为这是一个正常页面，从而进行收录。
而一旦重复的页面过多，会降低网站的权重，因为百度等会认为这是恶意竞争。

# 关于Request cookie
scrapy/downloadermiddlewares/cookies

# ip代理
西刺

tor
http://pkmishra.github.io/blog/2013/03/18/how-to-run-scrapy-with-TOR-and-multiple-browser-agents-part-1-mac/

# 验证码识别
* tesseract-ocr
识别率很低
* 在线打码
* 人工打码

## 云打码
http://www.yundama.com

* 用户账号
youxingzhi 81051766

* 开发者账号

# 动态网页抓取selenium
* 浏览器自动化测试框架
* python api

    http://selenium-python.readthedocs.io/api.html
    
# phantomjs，无界面的浏览器
多进程情况下其性能下降很严重

# 其他动态网页获取技术
* pyvirtualdisplay
* selenium grid
* splinter

# 暂停，重启
```javascript
scrapy crawl lagou -s JOBDIR=job_info/001
```

如果此时``ctrl+c``停止，爬虫会先处理掉已经发出去的request然后再停止，然后保存爬虫状态

# scrapy 去重原理
``scrapy->dupefilters``

# telnet
```javascript
telnet localhost:6023
```

# 状态收集器

# 信号

# 拓展
利用信号来实现一些切面编程