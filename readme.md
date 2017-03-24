# mysql下载
https://dev.mysql.com/downloads/installer/

# python豆瓣源
pip install *** -i https://pypi.douban.com/simple/

# virtualenv
以python3创建一个目录

virtualenv -p E:\soft\Python36\python.exe testProject

## vcruntime140.dll缺失
把python3中的该文件拷贝到virtualenv创建的目录下的Scripts下面

# virtualenvwrapper
## 安装
pip install virtualenvwrapper-win
## 设置工作目录
WORKON_HOME
## deactivate
## workon **
## mkvirtualenv --python=path\python.exe project
如果还是报vcruntime140.dll缺失，可用``virtualenv -p E:\soft\Python36\python.exe testProject``创建

# windows下包安装出错
www.lfd.uci.edu/~gohlke/pythonlibs/