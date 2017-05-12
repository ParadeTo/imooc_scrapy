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
```
telnet localhost:6023
```

# 状态收集器

# 信号

# 拓展
利用信号来实现一些切面编程

# core/scheduler
核心函数：
## enqueue_request
```
pqclass = load_object(settings['SCHEDULER_PRIORITY_QUEUE'])
dqclass = load_object(settings['SCHEDULER_DISK_QUEUE'])
mqclass = load_object(settings['SCHEDULER_MEMORY_QUEUE'])
```

在setting/default_settings.py

```
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleLifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.LifoMemoryQueue'
SCHEDULER_PRIORITY_QUEUE = 'queuelib.PriorityQueue'
```

```
# 状态保存到磁盘jbdir
dqok = self._dqpush(request)
...
self.dqs.push(reqd, -request.priority)
```


# bloomfilter的原理
http://blog.csdn.net/lmh12506/article/details/7575651

# redis setbit
set mykey 7 1 # 从左往右第8位设置为1

set mykey 32 1 # \x00\x00\x00\x00\x80

# elasticsearch
## elk 日志分析系统
## 安装及使用
1.安装jdk (>=8)

2.安装elasticsearch-rtf

github

3.head插件(类似navicat)和kibana插件(操作elasticsearch)

github

* head连接不了的解决办法
启动elasticsearch时候进行配置
```javascript
http.cors.enabled: true
http.cors.allow-origin: "*"
http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE
http.cors.allow-headers: "X-Requested-With, Content-Type, Content-Length, X-User"
```

* kibana版本与elasticsearch-rtf要一致
## 概念
|elasticsearch|mysql|
|--------------|-----|
|index(索引)|数据库|
|type(类型)|表|
|documents(文档)|行|
|fiels|列|

* 索引还可以做动词

## 倒排索引
TF-IDF

* 大小写转换
* 词干抽取 looking look应该为一个词
* 分词
* 倒排索引文件过大－压缩编码

## kibana操作
```
PUT lagou
{
  "settings": {
    "index": {
      "number_of_shards": 5,
      "number_of_replicas": 1
    }
  }
}

GET lagou/_settings
GET _all/_settings
GET .kibana,lagou/_settings

PUT lagou/_settings
{
  "number_of_replicas": 1
}

GET _all

# index/type/document(不指定会自动不指定会自动gen)
PUT lagou/job/1
{
  "title": "python分布式爬虫开发",
  "salary_min": 15000,
  "city": "北京",
  "company": {
    "name": "百度",
    "companyy_addr": "北京市软件园"
  },
  "publish_date": "2017-04-16",
  "comments": 15
}

GET lagou/job/1
GET lagou/job/1?_source=title

POST lagou/job/1/_update
{
  "doc": {
    "comments": 20
  }
}

DELETE lagou/job/1
DELETE lagou/job

# mget
PUT testdb/job1/1
{
  "title": "job1_1"
}
PUT testdb/job1/2
{
  "title": "job1_2"
}
PUT testdb/job2/1
{
  "title": "job2_1"
}
PUT testdb/job2/2
{
  "title": "job2_2"
}


GET _mget
{
  "docs": [
    {
      "_index": "testdb",
      "_type": "job1",
      "_id": "1"
    },
    {
      "_index": "testdb",
      "_type": "job2",
      "_id": "2"
    }
  ]
}

GET testdb/_mget
{
  "docs": [
    {
      "_type": "job1",
      "_id": "1"
    },
    {
      "_type": "job2",
      "_id": "2"
    }
  ]
}

GET testdb/job1/_mget
{
  "ids": [1, 2]
}

# bulk must in one line
# all opr will be passed to one node, the node deliver the opr to other replicas acoording to meta info, and receive the response from them, then return. 
POST _bulk
{"index": { "_index": "lagou","_type": "job","_id": "2" }}
{  "title": "python分布式爬虫开发2",  "salary_min": 16000,  "city": "北京",  "company": {"name": "百度", "companyy_addr":"北京市软件园2"  },"publish_date": "2017-04-17", "comments": 15}
{  "index": { "_index": "lagou","_type": "job", "_id": "3"}}
{  "title": "python分布式爬虫开发3",  "salary_min": 17000,  "city": "北京",  "company": {    "name": "百度",    "companyy_addr": "北京市软件园3"  },  "publish_date": "2017-04-18",  "comments": 15}

POST _bulk
{"update":{"_id":"1","_type":"type1","_index":"index1"}}
{"doc":{"field2":"value2"}}
```

## 映射（mapping）
elasticsearch会根据我们的数据自动映射属性的类型

### 内置类型
* text
* keyword(不会分析，不会建立倒排索引，查询时必须全部匹配到)
* 数字: long, integer, short, byte, double, float
* date
* boolean
* binary: will not retrieve
* object 
* nested: like array in javascript
* geo
* ip, competion

### 内置属性
* store: yes表示存储
* index：yes表示分析，默认true，适合string类型
* null_value: 字段默认值
* analyzer 分词器，默认为standard，可以用whitespace，simple，english
* include_in_all 如果某个字段不想被搜索到，可以设置为false
* format 时间格式字符串的模式，适合date

### example
一旦数据类型确定了，不能更改

```
PUT lagou
{
  "mappings": {
    "job": {
      "properties":{
        "title":{
          "type":"text"
        },
        "salary_min":{
          "type":"integer"
        },
        "city":{
          "type":"keyword"
        },
        "company":{
          "properties": {
            "name": {
              "type":"text"
            },
            "company_addr":{
              "type":"text"
            },
            "employee_count":{
              "type":"integer"
            }
          }
        },
        "publish_date":{
          "type":"date",
          "format":"yyyy-MM-dd"
        },
        "comments":{
          "type":"integer"
        }
      }
    }
  }
}

GET lagou/_mapping

PUT lagou/job/1
{
  "title": "python分布式爬虫开发",
  "salary_min": 15000,
  "city": "北京",
  "company": {
    "name": "百度",
    "companyy_addr": "北京市软件园",
    "employee_count": 44
  },
  "publish_date": "2017-04-16",
  "comments": 15
}
```

## 查询
* 基本查询
* 组合查询
* 过滤

```
# match
# 会对查询的内容进行分词，只要分词中有一个匹配即可
GET lagou/job/_search
{
	"query": {
		"match": {
			"title": "python"
		}
	}
}

# term
# 不会对查询词做处理
GET lagou/job/_search
{
	"query": {
		"term": {
			"title": "python"
		}
	}
}

# terms
# 数组中有匹配就返回
GET lagou/job/_search
{
	"query": {
		"terms": {
			"title": ["python","爬虫"]
		}
	}
}

# 控制返回数量，可用作分页
GET lagou/job/_search
{
	"query": {
		"match": {
			"title": "python"
		}
	},
	"from":1, # 开始的index 从0开始
	"size":2 # 数量
}

# match_all
GET lagou/job/_search
{
	"query": {
		"match_all": {}
	}
}

# match_phrase 短语查询
GET lagou/_search
{
	"query": {
		"match_phrase": {
			"title": {
				"query": "python系统", # 分词，且必须满足所有的词
				"slop": 6 # 分词之间的最小距离python与系统之间的距离必须小于3
			}
		}
	}
}

# multi_match 
GET lagou/job/_search
{
	"query": {
		"multi_match": {
			"query": "python",
			"fields":["title^3", "desc"] # title desc两者中满足其一 ^3表示权重，选择回来的结果其分数会比较高
		}
	}
}

# 返回特定字段
GET lagou/job/_search
{
	"stored_fields":["title","company_name"], # 返回的字段
	"query": {
		"match": {
			"title": "python"
		}
	}
}

# sort
GET lagou/job/_search
{
	"query": {
		"match_all": {}
	},
	"sort": [{
		"comments":{
			"order":"desc"
		}
	}]
}

# range
GET lagou/job/_search
{
	"query": {
		"range": {
			"comments": {
				"gte": 10,
				"lte": 20,
				"boost": 2.0 # 权重
			}
		}
	}
}

GET lagou/job/_search
{
	"query": {
		"range": {
			"add_time": {
				"gte": "2017-04-01",
				"lte": "now",
			}
		}
	}
}

# wildcard 模糊查询
GET lagou/job/_search
{
	"query": {
		"wildcard": {
			"title": {
				"value": "pyth*n",
				"boost": 2.0,
			}
		}
	}
}
```

## bool查询
```
bool: {
	"filter":[], # 过滤，不参与打分
	"must":[], # 都必须满足
	"should":[], # 满足至少一个
	"must_not":[] # 一个都不满足
}
```

### example
```
# select * from testjob where salary=20
GET lagou/testjob/_search
{
	"query": {
		"bool": {
			"must":{
				"match_all":{}
			},
			"filter":{
				"term":{
					"salary":[10, 20]
				}
			}
		}
	}
}

# select * from testjob where title="Python"
GET lagou/testjob/_search
{
	"query": {
		"bool": {
			"must":{
				"match_all":{}
			},
			"filter":{
				"term":{
					"title": "Python" # Python为text类型，入库的时候已经转为小写了，可以将term改为match
				}
			}
		}
	}
}

# select * from testjob where (salary=20 or title=Python) AND (price != 30)
GET lagou/testjob/_search
{
	"query": {
		"bool": {
			"should": [
				{"term":{"salary":20}},
				{"term":{"title":"python"}}
			],
			"must_not": {
				"term":{"price":30}
			}
		}
	}
}

# 嵌套查询
# select * from testjob where title="python" or (title="elasticsearch" AND salary=30)
GET lagou/testjob/_search
{
	"query": {
		"bool": {
			"should": [
				{"term":{"title":"python"}},
				{
					"bool":{
						"must":[
							{"term":{"title":"elasticsearch"}},
							{"term":{"salary":30}},
						]
					}
				}
			]
		}
	}
}

# 过滤空和非空
# select tags from testjob where tags is not null
GET lagou/testjob/_search
{
	"query": {
		"bool": {
			"filter": {
				"exists": {
					"field":"tags"
				}
			}
		}
	}
}

# select tags from testjob where tags is null 或者该字段不存在也可以
GET lagou/testjob/_search
{
	"query": {
		"bool": {
			"must_not": {
				"exists": {
					"field":"tags"
				}
			}
		}
	}
}





# 查看分析器解析的结果
GET _analyze
{
	"analyzer": "ik_max_word",
	"text": "Python网络开发工程师"
}

# completion suggestor 自动补全，详见官网文档
# https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html


# fuzzy模糊搜索
GET jobbole/article/_search
{
  "query": {
    "fuzzy": {
      "title":{
        "value": "linux",
        "fuzziness": 2,
        "prefix_length": 0
      }
    }
  }
}

# suggest
GET lagou/testjob/_search
{
	"suggest": {
		"my-suggest": {
			"text":"linux" # linu linxx 等都可以搜到linux
			"completion": {
				"field": "suggest",  # 自己生成的suggest字段
				"fuzzy":{
					"fuzziness":2
				}
			}
		}
	}
}
```

## scrapy数据写到es中
elasticsearch-dsl-py

https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#doctype

```
pip install elasticsearch-dsl
```