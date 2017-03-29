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
## jobbole article
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8;