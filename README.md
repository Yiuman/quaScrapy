# 去哪儿网（景区与景区评论信息爬虫）

>可爬取到去哪儿网景区搜索中相关地区的景区数据，QuaSpider蜘蛛中的keywords字段就是搜索关键字的一个数组,会自动翻页爬取数组中的地区景区以及景区相关的评论数据。

## 配置
在主项目下的，settings.py文件中可以配置mysql相关配置与链接池配置:
```python
MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'yiuman'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'yiuman'
MYSQL_PORT = 3306
INIT_TABLE_SQL_FILE = 'qua.sql'

PROXIES = [
    '119.41.207.206:8118',
    '115.219.40.107:8118',
    '182.149.157.235:8118',
    '171.41.161.51:8118',
    '112.80.158.109:8118',
    '122.193.122.161:8118',
]
```

## 运行
```python
    直接运行 scrapy crawl qua
    传参运行 scrapy crawl qua -a keywords=['阳山','连山']
```


